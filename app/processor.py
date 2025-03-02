# This is going to be the main file that will be used to process the transcripts.

YT_BASE_URL = 'https://www.youtube.com/watch?v='


def make_markdown(path: str):
    with open(path, 'r', encoding='utf-8') as f:
        text = f.read()
    file_name = path.split('\\')[-1].split('.')[0]
    chunks = file_name.split('_')
    transcript_id = chunks[-1]
    video_id = chunks[-2]
    title = ' '.join(chunks[1:-2])
    print(transcript_id, video_id, title, sep='\n')
    with open(f'files/{file_name}.md', 'w', encoding='utf-8') as f:
        f.write(f'# [{title}]({YT_BASE_URL}{video_id})\n\n')
        f.write(f'transcript_id: {transcript_id}\n\n')
        f.write(text)

path = r'F:\User\Data\Endeavors\Speech2Text\files\transcript_Rabbi Sends STRONG Message To The World From Jerusalem_X7Iav-Cr2C8_f5bbfeb7-fd78-4999-a947-1edfb3f17ff5.txt'

make_markdown(path)