import yt_dlp
from config import *


def pull_soundtrack(url: str, dst_dir='files'):
    ydl_opts = {
    'format': 'm4a/bestaudio/best',  # The best audio version in m4a format
    'outtmpl': f'{dst_dir}/%(title)s_%(id)s.%(ext)s',  
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)
        audio_file = ydl.prepare_filename(info)

    print(f'\n>>> Downloaded to: {audio_file}')
    return audio_file


def main():
    url = input('Enter the URL of the video: ')
    if not url:
        url = 'https://www.youtube.com/watch?v=wtolixa9XTg'
    pull_soundtrack(url)


if __name__ == '__main__':
    main()