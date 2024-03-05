from moviepy.editor import VideoFileClip
from pytube import YouTube
import sys





def download_audio_from_youtube(url, output_path='output.wav'):
    try:
        # Step 1: Download YouTube video
        yt = YouTube(url)
        video_stream = yt.streams.filter(file_extension='mp4').first()
        video_stream.download(filename='temp_video.mp4')

        # Step 2: Convert the downloaded video to wav format
        video_clip = VideoFileClip('temp_video.mp4')
        video_clip.audio.write_audiofile(output_path)

        # print(f'Audio downloaded and saved as {output_path}')

    except Exception as e:
        print(f'Error: {str(e)}')

# youtube_url = 'https://www.youtube.com/watch?v=cVDASbWZ_KI'
# if __name__ == '__main__':
#     # Replace with the actual YouTube video URL

#     download_audio_from_youtube(youtube_url)


sys.modules[__name__] = download_audio_from_youtube
