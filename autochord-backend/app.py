from flask import Flask, request, jsonify
from flask_cors import CORS
import extract_chords
from database import init_connection_pool, init_database, get_cache_stats, get_cached_chords, check_multiple_cached

app = Flask(__name__)
CORS(app)


@app.route('/link', methods=["POST"], strict_slashes=False)
def link():
    """Extract chords from a YouTube video URL"""
    try:
        link = request.json['linkpost']
        print(f"Received request for: {link}")
        result = extract_chords(link)
        print(f"Successfully extracted chords")
        return result
    except Exception as e:
        import traceback
        print(f"Error: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        return jsonify({"error": str(e)}), 500


@app.route('/health', methods=["GET"])
def health():
    """Health check endpoint"""
    return jsonify({"status": "ok"}), 200


@app.route('/cache/stats', methods=["GET"])
def cache_stats():
    """Get cache statistics"""
    try:
        stats = get_cache_stats()
        return jsonify(stats), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/cache/check', methods=["POST"])
def check_cache():
    """Check if a YouTube video is cached"""
    try:
        url = request.json['url']
        cached_data = get_cached_chords(url)
        return jsonify({"cached": cached_data is not None}), 200
    except Exception as e:
        return jsonify({"cached": False}), 200


@app.route('/cache/check-batch', methods=["POST"])
def check_cache_batch():
    """Check cache status for multiple YouTube videos at once"""
    try:
        video_ids = request.json.get('video_ids', [])

        if not video_ids:
            return jsonify({"error": "No video_ids provided"}), 400

        # Check cache status for all videos in one query
        cache_status = check_multiple_cached(video_ids)

        return jsonify({"cache_status": cache_status}), 200
    except Exception as e:
        print(f"Error in batch cache check: {e}")
        # Return all as uncached on error
        video_ids = request.json.get('video_ids', [])
        return jsonify({"cache_status": {vid: False for vid in video_ids}}), 200


if __name__ == '__main__':
    print("=" * 60)
    print("🎸 Starting Chord Extractor Backend...")
    print("=" * 60)

    # Initialize database
    print("\n📊 Initializing database connection...")
    if init_connection_pool():
        print("✅ Database connected!")
        init_database()

        # Show cache stats
        stats = get_cache_stats()
        if stats:
            print(f"   Cached songs: {stats['total_cached_songs']}")
    else:
        print("⚠️  Database not available - running without cache")
        print("   (All requests will process from scratch)")

    print("\n📡 Server running on http://127.0.0.1:5000")
    print("✅ CORS enabled for frontend")
    print("=" * 60 + "\n")

    app.run(debug=True, host='0.0.0.0', port=5000)


# url = 'https://www.youtube.com/watch?v=cEWwJxEq9Lg'
# download_audio_from_youtube(url)

# audio_file = librosa.load('output.wav')
# y, sr = audio_file

# tempo, beat_frames = librosa.beat.beat_track(y=y, sr=sr)
# print('Estimated tempo: {:.2f} beats per minute'.format(tempo))
# beat_times = librosa.frames_to_time(beat_frames, sr=sr)
# # print(tempo)
# beat = 60/tempo
# print(f"beat is {beat}")

# # print(beat_times)
# # sum = 0
# # for i in range(900):
# #     # print(beat_times[i+1] - beat_times[i])
# #     sum+=(beat_times[i+1]-beat_times[i])
# # print(f"beat avg is {sum/900}")

# chords = autochord.recognize('somewhere.wav', lab_fn='chords.lab')

# # for c in chords:
# #     print((c[1]-c[0])/0.510839)
# # chordName = ['Ab:maj','Db:maj','F:min','Eb:maj']

# ch = []

# # for i in chords:
# #     if i[2] in chordName:
# #         ch.append(i)

# for i in chords:
#     ch.append(i)

# # print(ch)

# # for i in chords:
# #     if i[2] in chordName:
# #         print(i[0],'\t',i[1],'\t',i[2],'\t',round(i[0]/beat))
#     # print(round(i[0],2),'\t',round(i[1],2),'\t',i[2])

# # print(chords)

# result = json.dumps(ch)
# print(result)
