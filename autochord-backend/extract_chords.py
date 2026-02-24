import json
import librosa
import autochord
import download_audio_from_youtube
import sys
import warnings

# Import database functions
from database import get_cached_chords, save_chords_to_cache

# Import music21 for key detection (may have numpy warnings)
try:
    with warnings.catch_warnings():
        warnings.simplefilter("ignore")
        from music21 import converter, chord as m21_chord, key as m21_key
    MUSIC21_AVAILABLE = True
except Exception as e:
    print(f"⚠️  music21 not available for key detection: {e}")
    MUSIC21_AVAILABLE = False


def detect_musical_key(chords_list):
    """
    Detect the musical key of a song from its chord progression.

    This uses music21's key detection algorithm which analyzes the
    frequency of notes in the chords to determine the most likely key.

    Parameters:
    - chords_list: List of tuples [(start, end, chord_name), ...]

    Returns:
    - dict: {"key": "C Major", "key_flat": "C Major", "key_sharp": "C Major"}

    📚 How it works:
    1. Parses each chord name into actual notes (e.g., "Cmaj" -> C, E, G)
    2. Counts the frequency of each note
    3. Uses the Krumhansl-Schmuckler algorithm to find the best key
    """
    if not MUSIC21_AVAILABLE:
        return {"key": "Unknown", "key_flat": "Unknown", "key_sharp": "Unknown"}

    try:
        from music21 import stream, note

        # Collect all chord names and convert autochord format to music21 format
        chord_names = []
        for start, end, chord_name in chords_list:
            if chord_name and chord_name != 'N':  # Skip 'N' (no chord)
                # Convert autochord format to music21 format
                # autochord uses: "A:maj", "A:min", "Gb:min", "Db:maj7", etc.
                chord_clean = chord_name.replace(':', '')  # Remove colon

                # Handle minor chords: "Gbmin" or "Gb-" -> "G-flat-minor"
                # music21 uses 'm' or 'minor' for minor chords
                if 'min' in chord_clean:
                    # Replace 'min' with 'm' for music21
                    chord_clean = chord_clean.replace('min', 'm')
                elif chord_clean.endswith('-'):
                    # autochord sometimes uses '-' for minor (e.g., "Gb-")
                    # Already good for music21, but need to handle flat notes
                    pass

                # Handle major chords: "Amaj" -> "A"
                chord_clean = chord_clean.replace('maj', '')

                # Convert flat notation for music21: "Gb" -> "G-" (music21 style)
                # But actually music21 understands "Gb", "Db", etc. directly!

                if chord_clean:  # Only add non-empty chords
                    chord_names.append(chord_clean)

        if not chord_names:
            return {"key": "Unknown", "key_flat": "Unknown", "key_sharp": "Unknown"}

        # Create a stream and add all chord notes
        s = stream.Stream()
        for chord_name in chord_names:
            try:
                # Parse the chord and add its notes to the stream
                c = m21_chord.Chord(chord_name)
                for pitch in c.pitches:
                    n = note.Note(pitch)
                    s.append(n)
            except Exception as e:
                # Skip unparseable chords (but don't print for every chord)
                continue

        if len(s.notes) == 0:
            return {"key": "Unknown", "key_flat": "Unknown", "key_sharp": "Unknown"}

        # Analyze key using music21's key detection
        key_result = s.analyze('key')

        # Get the key name - just the root note, no major/minor
        key_str = str(key_result)

        # Extract just the root note (remove "major" or "minor")
        # "f# minor" -> "F#", "a major" -> "A", "g minor" -> "G"
        key_parts = key_str.lower().split()
        if len(key_parts) >= 1:
            # Take first part (the note) and capitalize first letter only
            root_note = key_parts[0]
            # Handle sharp/flat symbols: "f#" -> "F#", "gb" -> "Gb"
            if len(root_note) > 1 and root_note[1] in ['#', 'b']:
                key_str = root_note[0].upper() + root_note[1]  # "F#" or "Gb"
            else:
                key_str = root_note[0].upper()  # Just "G" or "A"

        # Convert to flat notation
        key_flat = key_str.replace('C#', 'Db').replace('D#', 'Eb').replace(
            'F#', 'Gb').replace('G#', 'Ab').replace('A#', 'Bb')

        # Convert to sharp notation
        key_sharp = key_str.replace('Db', 'C#').replace('Eb', 'D#').replace(
            'Gb', 'F#').replace('Ab', 'G#').replace('Bb', 'A#')

        return {
            "key": key_str,  # Just root note
            "key_flat": key_flat,
            "key_sharp": key_sharp
        }

    except Exception as e:
        print(f"⚠️  Key detection error: {e}")
        import traceback
        traceback.print_exc()
        return {"key": "Unknown", "key_flat": "Unknown", "key_sharp": "Unknown"}
# url = 'https://www.youtube.com/watch?v=cEWwJxEq9Lg'


def extract_chords(url):
    """
    Extract chords from a YouTube video URL.

    📚 Workflow:
    1. Check cache first (fast!)
    2. If not cached, download and process:
       - Download audio from YouTube
       - Extract tempo and beats using librosa
       - Recognize chords using autochord
       - Detect musical key using music21
    3. Save to cache for future requests

    Returns JSON with: beat, bpm, key, chords, url
    """

    # Step 1: Check cache first
    print(f"🔍 Checking cache for {url}")
    cached_data = get_cached_chords(url)

    if cached_data:
        # Cache hit! Return cached data
        print(f"✅ Using cached data")

        # Generate flat/sharp variants from cached key
        key_str = cached_data['key']
        key_flat = key_str.replace('C#', 'Db').replace('D#', 'Eb').replace(
            'F#', 'Gb').replace('G#', 'Ab').replace('A#', 'Bb')
        key_sharp = key_str.replace('Db', 'C#').replace('Eb', 'D#').replace(
            'Gb', 'F#').replace('Ab', 'G#').replace('Bb', 'A#')

        jso = {
            "beat": cached_data['beat_length'],
            "bpm": cached_data['bpm'],
            "key": key_str,
            "key_flat": key_flat,
            "key_sharp": key_sharp,
            "chords": json.loads(cached_data['chords']) if isinstance(cached_data['chords'], str) else cached_data['chords'],
            "url": url,
            "title": cached_data['title'],
            "cached": True
        }
        return json.dumps(jso)

    # Step 2: Not in cache, extract chords
    print(f"⚙️  Extracting chords (not in cache)...")

    # Download audio
    video_info = download_audio_from_youtube(url)
    title = video_info.get('title', 'Unknown')
    duration = video_info.get('duration', 0)

    # Load audio and analyze
    audio_file = librosa.load('output.wav')
    y, sr = audio_file

    # Extract tempo and beats
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    beat = 60/tempo

    # Recognize chords
    chords = autochord.recognize('output.wav', lab_fn='chords.lab')
    ch = []
    for i in chords:
        ch.append(i)

    # Detect musical key
    print(f"🎼 Detecting musical key...")
    key_info = detect_musical_key(ch)
    print(
        f"   Key detected: {key_info['key']} (♭: {key_info['key_flat']}, ♯: {key_info['key_sharp']})")

    # Step 3: Save to cache (store the original key)
    save_chords_to_cache(
        youtube_url=url,
        title=title,
        duration=duration,
        beat_length=beat,
        bpm=float(tempo),
        key=key_info['key'],  # Store original key
        chords=ch
    )

    jso = {
        "beat": beat,
        "bpm": float(tempo),
        "key": key_info['key'],
        "key_flat": key_info['key_flat'],
        "key_sharp": key_info['key_sharp'],
        "chords": ch,
        "url": url,
        "title": title,
        "cached": False
    }

    return json.dumps(jso)


sys.modules[__name__] = extract_chords
