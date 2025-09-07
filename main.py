from YTdownload import *
from gui import App

#url = 'https://youtu.be/dQw4w9WgXcQ' #Rickroll
#url = 'https://youtu.be/3glOUPtVIpU' #901 shelby drive

# https://youtu.be/dQw4w9WgXcQ https://youtu.be/3glOUPtVIpU

def main():
    url_list = ['https://youtu.be/3glOUPtVIpU']
    format = 'mp4'

    if len(sys.argv) > 1:
        format = sys.argv[1] if sys.argv[1] in ('mp3', 'mp4') else 'mp4'
        url_list = sys.argv[2:] if sys.argv[1] in ('mp3', 'mp4') else sys.argv[1:]

        YTdownload(url_list, format)

    else:
        App()

if __name__ == '__main__':
    main()