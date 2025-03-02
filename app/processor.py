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
    with open(f'files/{file_name}.md', 'w', encoding='utf-8') as f:
        f.write(f'# [{title}]({YT_BASE_URL}{video_id})\n\n')
        f.write(f'transcript_id: {transcript_id}\n\n')
        f.write(text)


def main():
    path = input('Enter the path to the transcript file: ')
    make_markdown(path)
    print('Markdown file created.')


if __name__ == '__main__':
    main()