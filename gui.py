import customtkinter as ctk
from settings import *
from ui_components import *
from YTdownload import YTdownload, YT_video_info
import threading, platform, subprocess, os
from pathlib import Path
from tkinter import filedialog

ctk.set_default_color_theme('Anthracite.json')

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color = APP_BG_COLOR)

        #center window on screen
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        x = width // 2 - (APP_SIZE[0] //2)
        y = height // 2 - (APP_SIZE[1] // 2)

        #general window setup
        self.title(TITLE)
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}+{x}+{y}')
        self.minsize(MIN_SIZE[0], MIN_SIZE[1])

        #variables
        self.FormatVar = ctk.StringVar(value = FORMAT_VALUES[0])
        self.SubtitleVar = ctk.StringVar(value = SUBTITLE_VALUES[0])
        self.UrlVar = ctk.StringVar(value = '')
        self.ProgressStr = ctk.StringVar(value = '')
        self.SaveLocationStr = ctk.StringVar(value = str(Path.home() / "Downloads"))

        self.DownloadPercent = ctk.DoubleVar(value = 0)
        self.VideoInfoDict = None

        self.VideoInfoFrame = None
        self.ProgressBarFrame = None

        #widgets
        self.create_widgets()

        self.mainloop()

    def create_widgets(self):
        self.Title = TitleLabel(self)
        self.UrlFrame = UrlFrame(self, self.UrlVar, self.get_video_info)
        self.OptionButtonsFrame = OptionButtonsFrame(self, self.FormatVar, self.SubtitleVar, self.UrlVar)

    def download(self):
        if not self.VideoInfoDict:
            self.get_video_info()

        subtitle_bool = False if self.SubtitleVar.get() == SUBTITLE_VALUES[0] else True
        self.ProgressBarFrame = DownloadProgressFrame(self, self.DownloadPercent, self.ProgressStr, self.open_save_location)

        #run background thread
        threading.Thread(target = YTdownload,
                         args = (self.progress_hook, [self.UrlVar.get()], self.FormatVar.get(), subtitle_bool),
                         daemon = True).start()

    def get_video_info(self):
        if self.VideoInfoFrame:
            self.VideoInfoFrame.destroy()

        self.VideoInfoDict = YT_video_info(self.UrlVar.get())
        self.video_title = self.VideoInfoDict['title']
        self.channel = self.VideoInfoDict['channel']
        self.video_duration = f'{self.VideoInfoDict['duration'] // 60} m : {self.VideoInfoDict['duration']%60} s'
        self.thumbnail = self.VideoInfoDict['thumbnail']

        if self.VideoInfoDict:
            self.VideoInfoFrame = VideoInfoFrame(self, self.video_title, self.video_duration, self.channel, self.thumbnail)

    def progress_hook(self, d):
        downloaded = d.get('downloaded_bytes', 0)
        total = d.get('total_bytes', 1)
        percent_float = downloaded / total 

        progress_str = f'{round((percent_float*100),1)}% of {d.get('_total_bytes_str').strip()}\nSpeed: {d.get('_speed_str', '').strip()} ETA: {d.get('_eta_str', '').strip()}'

        if percent_float*100 >= 100:
            progress_str = f'Download Finished'

        self.ProgressStr.set(progress_str)
        self.DownloadPercent.set(percent_float)

    def open_save_location(self):
        system = platform.system()

        if system == "Windows":
            subprocess.run(f'explorer /select,"{self.SaveLocationStr.get()}"')
        elif system == "Darwin": #macOS
            subprocess.run(["open", "-R", self.SaveLocationStr.get()])
        elif system == "Linux":
            subprocess.run(["xdg-open", os.path.dirname(self.SaveLocationStr.get())])
        else:
            raise NotImplementedError(f"OS {system} not supported")


class TitleLabel(ctk.CTkLabel):
    def __init__(self, parent):
        super().__init__(master = parent,
                       text = 'YT Downloader',
                       font = ctk.CTkFont(*TITLE_FONT_DATA),
                       text_color = FONT_COLOR)

        self.place(relx = 0.5,
                   rely = 0.05,
                   relwidth = 1,
                   relheight = 0.1,
                   anchor = 'center',)

    
class UrlFrame(ctk.CTkFrame):
    def __init__(self, parent, url_var, get_video_info_func):
        super().__init__(master = parent,
                         fg_color = 'transparent',
                         border_width = 0)
        
        self.widget_font = ctk.CTkFont(*WIDGET_FONT_DATA)
        self.UrlVar = url_var

        self.place(relx = 0,
                   rely = 0.15,
                   relwidth = 1,
                   relheight = 0.2,
                   anchor = 'nw')
        
        self.instruction = ctk.CTkLabel(self,
                                        font = self.widget_font,
                                        text = 'Insert a valid URL',
                                        text_color = FONT_COLOR)
        
        self.url_entry = ctk.CTkEntry(self,
                                      font = self.widget_font,
                                      corner_radius = 12,
                                      text_color = INPUT_FIELD_COLOR,
                                      textvariable = self.UrlVar)
        
        self.instruction.place(relx = 0.5,
                               rely = 0.2,
                               relheight = 0.2,
                               relwidth = 1,
                               anchor = 'center')
        
        self.url_entry.place(relx = 0.5,
                             rely = 0.6,
                             relwidth = 0.7,
                             relheight = 0.4,
                             anchor = 'center')
        
        self.url_entry.bind('<Return>', lambda e: get_video_info_func())


class OptionButtonsFrame(ctk.CTkFrame):
    def __init__(self, parent, format_var, subititle_var, url_var):
        super().__init__(master = parent,
                         fg_color = 'transparent',
                         border_width = 0)

        self.place(relx = 0,
                   rely = 0.35,
                   relwidth = 1,
                   relheight = 0.1,
                   anchor = 'nw')
    
        self.FormatVar = format_var
        self.SubtitleVar = subititle_var
        self.UrlVar = url_var
        self.MainWindow = parent

        self.format_selector = OptionSelector(self,
                                              values = FORMAT_VALUES,
                                              variable = self.FormatVar,
                                              relx = 0.15)
        
        self.subtitle_selector = OptionSelector(self,
                                                values = SUBTITLE_VALUES,
                                                variable = self.SubtitleVar,
                                                relx = 0.4)
        
        self.download_button = DownloadButton(self, command = self.MainWindow.download)


class VideoInfoFrame(ctk.CTkFrame):
    def __init__(self, parent, video_title, video_duration, video_author, thumbnail_url):
        super().__init__(master = parent,
                         fg_color = 'transparent',
                         border_width = 0)
        
        self.place(relx = 0,
                   rely = 0.45,
                   relwidth = 1,
                   relheight = 0.35,
                   anchor = 'nw')
        
        self.thumbnail_preview = ThumbnailPreview(self, thumbnail_url)
        self.title = VideoInfoLabel(self, 'Title', video_title, 0.55)
        self.duration = VideoInfoLabel(self, 'Duration', video_duration, 0.7)
        self.channel = VideoInfoLabel(self, 'Channel', video_author, 0.85)
        

class DownloadProgressFrame(ctk.CTkFrame):
    def __init__(self, parent, percent_var, progress_str, open_save_location_function):
        super().__init__(master = parent,
                         fg_color = 'transparent',
                         border_width = 0)
        
        self.place(relx = 0,
                   rely = 0.8,
                   relwidth = 1,
                   relheight = 0.2,
                   anchor = 'nw')
        
        self.proress_label = DownloadLabel(self, progress_str)
        self.progress_bar = DownloadProgressBar(self, percent_var)
        self.open_save_location_button = OpenSaveLocationButton(self, open_save_location_function)