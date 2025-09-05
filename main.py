import yt_dlp as dlp
import sys

#url = 'https://youtu.be/dQw4w9WgXcQ' #Rickroll
#url = 'https://youtu.be/3glOUPtVIpU' #901 shelby drive


ydl_opts = {
    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
    "merge_output_format": "mp4",
    "outtmpl": "%(title)s.%(ext)s",
}


if len(sys.argv) > 1:
    with dlp.YoutubeDL(ydl_opts) as ydl:
        for url in sys.argv[1:]:
            ydl.download([url])