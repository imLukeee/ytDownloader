import yt_dlp as dlp
from pathlib import Path
import os
import re


def sanitize_title(title: str) -> str: 
    title = title.replace('\u00A0', ' ')   # remove non-breaking spaces
    title = title.replace('\u200B', '')    # remove zero-width spaces
    title = re.sub(r'[<>:"/\\|?*\n\r\t]', '', title)
    title = re.sub(r'\s+', ' ', title).strip()
    return title


def YTdownload(progress_hook=None, url_list=None, format='mp4', subtitles=False, save_location=None, quality=None, cli=False):
    if not url_list:
        print("No URL provided.")
        return

    with dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url_list[0], download=False)
        info['title'] = sanitize_title(info['title'])
        clean_title = info['title']

    outtmpl_path = os.path.join(
        str(Path.home() / "Downloads") if save_location is None else save_location,
        f"{clean_title}.%(ext)s"
    )

    # default options
    ydl_options = {
        "format": f"bestvideo[{'bestvideo[height<={quality}]' if quality is not None else 'ext=mp4'}]+bestaudio[ext=m4a]/best[ext=mp4]",
        "merge_output_format": "mp4",
        "writesubtitles": subtitles,
        "subtitleslangs": ["en", "pl"],
        "subtitlesformat": "srt",
        "outtmpl": outtmpl_path,
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
            "preferredquality": "192",
        }]

    with dlp.YoutubeDL(ydl_options) as ydl:
        ydl.download(url_list)


def YT_video_info(url):
    with dlp.YoutubeDL() as ydl:
        info = ydl.extract_info(url, download=False)
        return {
            'title': sanitize_title(info.get('title')),  # 🔧 sanitized here too
            'duration': info.get('duration'),
            'channel': info.get('uploader'),
            'thumbnail': info.get('thumbnail'),
        }