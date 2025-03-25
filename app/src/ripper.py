import json

import yt_dlp

import assemblyai as aai

from config import *
aai.settings.api_key = aai_key  # Set the API key for AssemblyAI using externally stored value


def pull_soundtrack(url: str, dst_dir='files'):
    ydl_opts = {
    'format': 'm4a/bestaudio/best',  # The best audio version in m4a format
    'outtmpl': f'{dst_dir}/%(title)s_%(id)s.%(ext)s',  
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)
        audio_file = ydl.prepare_filename(info)  # TODO: Use info dic values to build the file name

    print(f'\n>>> Downloaded to: {audio_file}')
    return audio_file


def extract_subtitles(video_url: str, lang='th', output_path='files', skip_download=True):
    """Extract subtitles from a YouTube video and save them to a file.
    Args:
        video_url (str): The URL of the YouTube video.
        lang (str): The language code of the subtitles to extract.
        output_path (str): The path to save the subtitles file.
        skip_download (bool): Whether to skip downloading the video.
    :return: The path to the saved subtitles file.
    """
    ydl_opts = {
        'writesubtitles': True,
        'writeautomaticsub': True,  # Enable auto-generated subtitles
        'subtitleslangs': [lang],
        'skip_download': skip_download,
        'outtmpl': f'{output_path}/%(title)s_%(id)s.%(ext)s',
        'format': 'best'
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(video_url, download=True)
    subtitle_path = info['requested_subtitles'][lang]['filepath']
    return subtitle_path


def build_transcript(audio_file: str):
    transcriber = aai.Transcriber()
    print('building transcript...')
    transcript = transcriber.transcribe(audio_file)
    print(f'transcript {transcript.id} of {audio_file} ready.')
    
    file_name = audio_file.split("\\")[-1].split(".")[0]
    json.dump(
        transcript.json_response, 
        open(f'files/transcript_{file_name}_{transcript.id}.json', 'w', encoding='utf-8'), 
        indent=4, 
        ensure_ascii=False
    )
    print(f'transcript {transcript.id} of {file_name} saved as JSON.')
    with open(f'files/transcript_{file_name}_{transcript.id}.txt', 'w', encoding='utf-8') as f:
        f.write(transcript.text)
    print(f'transcript {transcript.id} of {file_name} saved as TXT.')


def pull_video(url: str):
    ydl_opts = {
    'format': 'bestvideo+bestaudio/best',  # The best video and audio version
    'outtmpl': 'files/%(title)s_%(id)s.%(ext)s',  # The output name will be the title and id followed by the extension
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url)
    video_file = ydl.prepare_filename(info)
    print(f'\n>>> Downloaded to: {video_file}')


def pull_and_transcribe(url: str):
    audio_file = pull_soundtrack(url)
    build_transcript(audio_file)


def main():
    action = None
    while action not in ['1', '2', '3', 'q']:
        if action:
            print('Invalid input. Please try again.')
        action = input(
            '''This worker can:
            - [1] build a transcript of locally stored media file;
            - [2] build a transcript of a YouTube video;
            - [3] pull a YouTube video and save it locally;
            Choose action, q to exit: '''
        )
    if action == 'q':
        return
    if action == '1':
        path = input('Path to local media file: ')
        build_transcript(path)
        return
    url = input('Enter the video URL: ')
    if not url:
        url = 'https://www.youtube.com/watch?v=wtolixa9XTg'
        print(f'using the demo url ({url})')
    if action == '2':
        pull_and_transcribe(url)
        print()
    elif action == '3':
        pull_video(url)
        print()
    

if __name__ == '__main__':
    main()