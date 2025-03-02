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
        audio_file = ydl.prepare_filename(info)

    print(f'\n>>> Downloaded to: {audio_file}')
    return audio_file


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
    url = input('Enter the video URL: ')
    if not url:
        url = 'https://www.youtube.com/watch?v=wtolixa9XTg'
        print(f'using the demo url ({url})')
    
    action = None
    while action not in ['v', 't', 'q']:
        if action:
            print('Invalid input. Please try again.')
        action = input('Do you want to pull a video(v) or to build a transcript thereof(t)? (v/t/ q to exit): ')
    if action == 'v':
        pull_video(url)
        print()
    elif action == 't':
        pull_and_transcribe(url)
        print()
    else:
        print('>>> Terminated by user.\n')
        return


if __name__ == '__main__':
    main()