# This is going to be the main file that will be used to process the transcripts.
import re
from datetime import datetime as dt
import pandas as pd

YT_BASE_URL = 'https://www.youtube.com/watch?v='
TIME_FORMAT = '%H:%M:%S.%f'


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


def match_timestamps_wth_auto_subs(vtt_file, min_duration=.1, save_tsv=True, save_txt=True):
    timestamps = []
    texts = []

    # Regular expression to match the timestamp pattern
    timestamp_pattern = re.compile(r'(\d{2}:\d{2}:\d{2}.\d{3}) --> (\d{2}:\d{2}:\d{2}.\d{3})')

    with open(vtt_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()
    for idx, line in enumerate(lines):
        match = timestamp_pattern.match(line.strip())
        if match:
            start_time, end_time = match.groups()
            delta = dt.strptime(end_time, TIME_FORMAT) - dt.strptime(start_time, TIME_FORMAT)
            if delta.total_seconds() > min_duration:    
                timestamps.append((start_time, end_time))
                text = lines[idx + 2].strip()
                texts.append(re.sub(r'<[^>]*>', '', text))
    stamped = list(zip(timestamps, texts))

    if save_tsv:
        with open(vtt_file.replace('.vtt', '.tsv'), "w", encoding="utf-8") as file:
            file.write("start_time\tend_time\ttext\n")
            for timestamp, text in stamped:
                file.write(f"{timestamp[0]}\t{timestamp[1]}\t{text}\n")

    if save_txt:
        with open(vtt_file.replace('.vtt', '.txt'), "w", encoding="utf-8") as file:
            for timestamp, text in stamped:
                file.write(f"{text}\n")
    
    return stamped


def find_timestamps(path: str):
    sub_df = pd.read_csv(path, sep='\t')
    print('Subtitle data loaded.' + '\n')
    while True:  # TODO: move the execution cycle to main()
        query = input('Enter the text to search for: ')
        if not query:
            break
        res = sub_df[sub_df['text'].str.contains(query)]
        build_console_response(res)
        # return res
        

def build_console_response(data: pd.DataFrame):
    if data.empty:
            print('No matches found.')
    else:
        print()
        for i, row in data.iterrows():
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