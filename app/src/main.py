import ripper as rpr
import processor as prc


def main():
    while True:
        action = input(
                'Choose action:\n'
                '\t[1] Extract subtitles\n'
                '\t[2] Build transcript\n'
                '\t[Enter] to quit: ' 
            )
        if not action:
            break
        if action not in ['1', '2']:
            print('Illegal action. Please reconsider')
            continue
        if action == '1':
            url = input('Enter the URL of the video: ')
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
        if action == '2':
            audio_file = input('Enter the path to the audio file: ')
            prc.build_transcript(audio_file)
            print(f'Transcript built from {audio_file}.')


if __name__ == '__main__':
    main()