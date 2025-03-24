# This is going to be the main file that will be used to process the transcripts.
import pandas as pd

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


def find_timestamps(path: str):
    sub_df = pd.read_csv(path, sep='\t')
    print('Subtitle data loaded.' + '\n')
    while True:
        query = input('Enter the text to search for: ')
        if not query:
            break
        res = sub_df[sub_df['text'].str.contains(query)]
        if res.empty:
            print('No matches found.')
        else:
            # print('\n', res[['start_time', 'end_time', 'text']], '\n')
            print()
            for i, row in res.iterrows():
                print(f'{row.start_time} -> {row.end_time}: {row.text}')
            print()
    

def main():
    while True:
        action = input('Enter "1" to find timestamps, "2" to create markdown: ')
        if not action:
            break
        if action not in ['1', '2']:
            print('Invalid action.')
            continue
        if action == '1':
            path = input('Enter path to the subtitles tsv: ')
            find_timestamps(path)
        if action == '2':
            path = input('Enter the path to the transcript file: ')
            make_markdown(path)
            print('Markdown file created.')


if __name__ == '__main__':
    main()