from moviepy.editor import VideoFileClip
from pytubefix import YouTube
import sys


def download_audio_from_youtube(url, output_path='output.wav'):
    """
    Download audio from YouTube and return video metadata.

    Returns:
    - dict: Video information (title, duration, etc.)
    """
    try:
        # Step 1: Download YouTube video
        yt = YouTube(url)
        video_stream = yt.streams.filter(file_extension='mp4').first()
        video_stream.download(filename='temp_video.mp4')

        # Step 2: Convert the downloaded video to wav format
        video_clip = VideoFileClip('temp_video.mp4')
        video_clip.audio.write_audiofile(output_path)

        # Return video metadata
        return {
            'title': yt.title,
            'duration': yt.length,
            'author': yt.author,
            'views': yt.views
        }

    except Exception as e:
        print(f'Error: {str(e)}')
        return {
            'title': 'Unknown',
            'duration': 0,
            'author': 'Unknown',
            'views': 0
        }

# youtube_url = 'https://www.youtube.com/watch?v=cVDASbWZ_KI'
# if __name__ == '__main__':
#     # Replace with the actual YouTube video URL

#     download_audio_from_youtube(youtube_url)


sys.modules[__name__] = download_audio_from_youtube
