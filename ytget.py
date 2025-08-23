#!/bin/python
#ytget.py
# Youtube downloader. Can parse files with specific structure.

####################################################|Libraries and Imports|######################################################
import click
import os
import subprocess
import sys
import yt_dlp
from random import randint
#######################################################|Color fuction|###########################################################
def printcolor(text, color="green"):
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m"
    }
    reset = "\033[0m"
    print(f"{colors.get(color, '')}{text}{reset}")
#####################################################|Filename Generation|#######################################################
def gen_filename():
    a = randint(1, 100000000)
    filename = "video" + str(a)
    return filename, a

def gen_filename1(a):
    filename1 = "audio" + str(a)
    return filename1
#####################################################|Download Function|########################################################
def download(url, format_choice):
    filename, a = gen_filename()
    filename1 = gen_filename1(a)

    ydl_opts = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'outtmpl': f'~/yt/audio+video/{filename}',
        'quiet': True,
        'no_warnings': False,
    }

    ydl_opts1 = {
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mkv',
        'outtmpl': f'~/yt/audio+video/{filename}',
        'quiet': True,
        'no_warnings': False,
    }

    ydl_opts_only_audio = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': f'~/yt/audio/{filename1}',
        'quiet': True,
        'no_warnings': False,
    }

    ydl_opts_only_video = {
        'format': 'bestvideo/best',
        'merge_output_format': 'mp4',
        'outtmpl': f'~/yt/video/{filename}.mp4',
        'quiet': True,
        'no_warnings': False,
    }

    printcolor("### Loading... ###", "green")

    try:
        if format_choice == 1:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            print("### Loading finished! ###")
            print("File saved as", filename)

        elif format_choice == 2:
            with yt_dlp.YoutubeDL(ydl_opts1) as ydl:
                ydl.download([url])
            print("### Loading finished! ###")
            print("File saved as", filename)

        elif format_choice == 3:
            with yt_dlp.YoutubeDL(ydl_opts_only_audio) as ydl:
                ydl.download([url])
            print("### Audio loading finished! ###")
            print("Audio saved as", filename1)

        elif format_choice == 4:
            with yt_dlp.YoutubeDL(ydl_opts_only_audio) as ydl:
                ydl.download([url])
            print("### Audio loading finished! ###")
            print("Audio saved as", filename1)

            with yt_dlp.YoutubeDL(ydl_opts_only_video) as ydl:
                ydl.download([url])
            print("### Video loading finished! ###")
            print("Video saved as", filename)

    except Exception as e:
        printcolor(f"Error during download: {e}", "red")

#########################################################|Parser Functions|############################################################
def parse_urls_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as file:
            content = file.read().strip()

        strings = content.split('\n')

        if len(strings) > 2:
            raise ValueError("File contains more than 2 strings")

        urls = []
        flags_string = ""

        if strings:

            first_string = strings[0].strip()
            cleaned_content = first_string.replace('{', ' ').replace('}', ' ').replace(',', ' ')
            potential_urls = [url.strip() for url in cleaned_content.split() if url.strip()]

            for url in potential_urls:
                if not url.startswith(('http://', 'https://')):
                    raise ValueError(f"Invalid URL format: {url}")
                if '&start_radio' in url:
                    printcolor("$start_radio tag is not appropriate! Ignoring URL...", "red")
                    continue
                urls.append(url)

            # Process flags if second string exists
            if len(strings) > 1:
                flags_string = strings[1].strip()

                if flags_string:
                    valid_flags = {'mp4', 'mkv', 'mp3', 'split'}
                    flags = flags_string.split()

                    for flag in flags:
                        if flag not in valid_flags:
                            raise ValueError(f"Unknown flag: '{flag}'. Valid flags are: {', '.join(valid_flags)}")

                    format_flags = [flag for flag in flags if flag in {'mp4', 'mkv', 'mp3'}]
                    if len(format_flags) > 1:
                        raise ValueError(f"Cannot use multiple format flags: {', '.join(format_flags)}")
        return urls, flags_string
    except FileNotFoundError:
        print(f"File {filename} is not found!")
        return [], ""
    except Exception as e:
        print(f"Parsing error!: {e}")
        return [], ""
#########################################################|Parser Processor|############################################################
def run_parser():
    file_path = input("Enter path to a file: ").strip()
    if not os.path.exists(file_path):
        printcolor(f"File {file_path} does not exist", "red")
        return
    urls, flags = parse_urls_from_file(file_path)
    if not urls:
        printcolor("Parsing error has occured.", "red")
        return
    printcolor("URL list:", "white")
    for i, url in enumerate(urls, 1):
        print(f"{i}. {url}")
    if flags:
        print(f"\nFlags: {flags}")
    print(f"\nTotal URLs: {len(urls)}")
    format_mapping = {'mp4': 1, 'mkv': 2, 'mp3': 3, 'split': 4}
    # Determine format choice from flags or default to mp4
    format_choice = 1  # Default to mp4
    if flags:
        flag_parts = flags.split()
        for flag in flag_parts:
            if flag in format_mapping:
                format_choice = format_mapping[flag]
                break
    for i, url in enumerate(urls, 1):
        printcolor(f"\nProcessing URL {i}/{len(urls)}: {url}", "green")
        download(url, format_choice)
#####################################################|Click Interface|##########################################################
@click.command()
@click.argument('url', required=False)
@click.option('--get', '-g', type=click.Choice(['mp4', 'mkv', 'mp3', 'split']), default='mp4',
              help='''Format choice:
              mp4 - MP4 (video+audio)
              mkv - MKV (video+audio)
              mp3 - MP3 (audio only)
              split - Both video and audio separately''')
@click.option('--parse', '-p', is_flag=True, help='Executes parse module.')
def main(url, get, parse):
    """Download youtube video/audio by providing some flags and URL or mass download from file. More in readme."""

    os.system('clear')

    if parse:
        run_parser()
        return

    if not url:
        click.echo("Error! No flags specified! Run with --help for basic documentation.")
        return

    format_mapping = {'mp4': 1, 'mkv': 2, 'mp3': 3, 'split': 4}
    format_choice = format_mapping[get]

    click.echo(f"Downloading from: {url}")
    click.echo(f"Selected format: {get}")
    download(url, format_choice)

if __name__ == '__main__':
    main()
