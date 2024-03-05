import json
import librosa
import autochord
import download_audio_from_youtube
import sys


# url = 'https://www.youtube.com/watch?v=cEWwJxEq9Lg'
def extract_chords(url):
    download_audio_from_youtube(url)
    audio_file = librosa.load('output.wav')
    y, sr = audio_file
    tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
    # print('Estimated tempo: {:.2f} beats per minute'.format(tempo))
    beat_times = librosa.frames_to_time(beat_frames, sr=sr)
    beat = 60/tempo
    chords = autochord.recognize('output.wav', lab_fn='chords.lab')
    ch = []
    for i in chords:
        ch.append(i)

    jso = {
        "beat":beat,
        "chords":ch,
        "url":url
    }
    
    return json.dumps(jso)

sys.modules[__name__] = extract_chords

