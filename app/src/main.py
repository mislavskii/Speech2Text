import ripper as rpr
import processor as prc


def harvest_from_video(url):
    while True:
        action = input(
            'Choose action:\n'
            '\t[1] Extract subtitles\n'
            '\t[2] Download video\n'
            '\t[3] Download soundtrack\n'
            '\t[Enter] to quit: ' 
        )
        if not action:
            break
        elif action == '1':  # extract subtitles
            lang = input('Enter the language code [th]: ')
            path = input('Enter the path to save the subtitles (defaults to `files`): ')
            download_video = input('Download and save the video? [y / Enter to skip]: ')
            subtitle_path = rpr.extract_subtitles(
                url, 
                lang = lang if lang else 'th',
                output_path = path if path else 'files',
                skip_download = False if download_video else True
            )
            print(f'Subtitles extracted to {subtitle_path}.')
        elif action == '2':
            rpr.pull_video(url)
        elif action == '3':
            rpr.pull_soundtrack(url)
        else:
            print('Unknown action. Please clarify.')


def main():
    while True:
        action = input(
                'Choose action:\n'
                '\t[1] Harvest from video url\n'
                '\t[2] Build transcript\n'
                '\t[3] Process transcript\n' 
                '\t[Enter] to quit: ' 
        )
        if not action:
            break
        if action not in ['1', '2']:
            print('Illegal action. Please reconsider')
            continue

        if action == '1':
            url = input('Enter the URL of the video: ')
            harvest_from_video(url)

        if action == '2':
            audio_file = input('Enter the path to the audio file: ')
            rpr.build_transcript(audio_file)
            print(f'Transcript built from {audio_file}.')


if __name__ == '__main__':
    main()