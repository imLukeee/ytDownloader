import yt_dlp as dlp
import sys

def YTdownload(url_list = None, format = 'mp4', subtitles = False, quality = None):
    #default options
    ydl_options = {
    "format": f"bestvideo[{'bestvideo[height<={quality}]' if quality != None else 'ext=mp4'}]+bestaudio[ext=m4a]/best[ext=mp4]",
    "merge_output_format": "mp4",
    "outtmpl": "%(title)s.%(ext)s",
    "writesubtitles": subtitles,
    "subtitleslangs": ["en", "pl"],
    "subtitlesformat": "srt"}

    if format.lower() == 'mp3':
        ydl_options["format"] = "bestaudio/best"
        ydl_options["postprocessors"] = [{
        "key": "FFmpegExtractAudio",
        "preferredcodec": "mp3",
        "preferredquality": "192",}]


    if url_list:
        with dlp.YoutubeDL(ydl_options) as ydl:
            ydl.download(url_list)
    else:
        print("No URL provided.")
