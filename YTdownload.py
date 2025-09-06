import yt_dlp as dlp
import sys

def YTdownload(url_list = None, format = 'mp4', subtitles = False, quality = None|int):
    ydl_opts = {
    "format": f"bestvideo[{'bestvideo[height<={quality}]' if quality != None else 'ext=mp4'}]+bestaudio[ext=m4a]/best[ext=mp4]",
    "merge_output_format": "mp4",
    "outtmpl": "%(title)s.%(ext)s",
    "writesubtitles": subtitles,
    "subtitleslangs": ["en"],
    "subtitlesformat": "srt"}

    if len(sys.argv) > 1:
        offset = 1
        if sys.argv[1] == 'mp3':
            ydl_opts["format"] = "bestaudio/best"
            ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",}]

            offset += 1

        with dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(sys.argv[offset:])
    
    else:
        if format == 'mp3':
            ydl_opts["format"] = "bestaudio/best"
            ydl_opts["postprocessors"] = [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",}]

        with dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(url_list)