import yt_dlp as dlp
import sys

#url = 'https://youtu.be/dQw4w9WgXcQ' #Rickroll
#url = 'https://youtu.be/3glOUPtVIpU' #901 shelby drive


ydl_opts = {
    "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]",
    "merge_output_format": "mp4",
    "outtmpl": "%(title)s.%(ext)s",
}

offset = 1

if len(sys.argv) > 1:
    if sys.argv[1] == 'mp3':
        ydl_opts["format"] = "bestaudio/best"
        ydl_opts["postprocessors"] = [{
    "key": "FFmpegExtractAudio",
    "preferredcodec": "mp3",
    "preferredquality": "192",
}]
        offset += 1
    with dlp.YoutubeDL(ydl_opts) as ydl:
        for url in sys.argv[offset:]:
            ydl.download([url])