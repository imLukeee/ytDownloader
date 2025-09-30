import yt_dlp as dlp
from pathlib import Path
import os

def YTdownload(progress_hook = None ,url_list = None, format = 'mp4', subtitles = False, save_location = None, quality = None, cli = False ):
    #default options
    ydl_options = {
    "format": f"bestvideo[{'bestvideo[height<={quality}]' if quality != None else 'ext=mp4'}]+bestaudio[ext=m4a]/best[ext=mp4]",
    "merge_output_format": "mp4",
    "writesubtitles": subtitles,
    "subtitleslangs": ["en", "pl"],
    "subtitlesformat": "srt",
    "outtmpl": os.path.join(str(Path.home() / "Downloads"), "%(title)s.%(ext)s") if save_location == None else os.path.join(save_location, "%(title)s.%(ext)s")
    }

    if not cli and progress_hook:
        ydl_options["progress_hooks"] = [progress_hook]
        ydl_options["quiet"] = True
        ydl_options["no_warnings"] = True
        ydl_options["no_color"] = True
        ydl_options["noprogress"] = True

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


def YT_video_info(url):
    with dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            'title': info.get('title'),
            'duration': info.get('duration'),
            'channel': info.get('uploader'),
            'thumbnail': info.get('thumbnail')
        }