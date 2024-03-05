from flask import Flask, request
from flask_cors import CORS
import extract_chords
app = Flask(__name__)
CORS(app)


@app.route('/link', methods=["POST"], strict_slashes=False)
def link():
    link = request.json['linkpost']
    return extract_chords(link)
    # return extract_chords(link)

    # with open("myfile.txt", "w+") as file1:

# print(link['body'])


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
