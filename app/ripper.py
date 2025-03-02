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


def pull_and_transcribe(url: str):
    audio_file = pull_soundtrack(url)
    build_transcript(audio_file)


def main():
    url = input('Enter the URL of the video: ')
    if not url:
        url = 'https://www.youtube.com/watch?v=wtolixa9XTg'
    pull_and_transcribe(url)


if __name__ == '__main__':
    main()