import customtkinter as ctk
from settings import *
from ui_components import *
from YTdownload import YTdownload, YT_video_info

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

        #variables
        self.FormatVar = ctk.StringVar(value = FORMAT_VALUES[0])
        self.SubtitleVar = ctk.StringVar(value = SUBTITLE_VALUES[0])
        self.UrlVar = ctk.StringVar(value = '')

        self.VideoInfoFrame = None
        self.ProgressBarFrame = None

        #widgets
        self.create_widgets()

        self.mainloop()

    def create_widgets(self):
        self.Title = TitleLabel(self)
        self.UrlFrame = UrlFrame(self, self.UrlVar, self.get_video_info)
        self.OptionButtonsFrame = OptionButtonsFrame(self, self.FormatVar, self.SubtitleVar, self.UrlVar)
        #self.VideoInfoFrame = VideoInfoFrame(self)
        #self.ProgressBarFrame = DownloadProgressFrame(self)

    def download(self):
        subtitle_bool = False if self.SubtitleVar.get() == SUBTITLE_VALUES[0] else True
        YTdownload([self.UrlVar.get()], self.FormatVar.get(), subtitle_bool)
        self.ProgressBarFrame = DownloadProgressFrame(self)

    def get_video_info(self):
        if self.VideoInfoFrame:
            self.VideoInfoFrame.destroy()

        info_list = YT_video_info(self.UrlVar.get())
        self.video_title, self.video_author = info_list[0], info_list[2]
        self.video_duration = f'{info_list[1] // 60}:{info_list[1]%60}'

        if info_list:
            self.VideoInfoFrame = VideoInfoFrame(self, self.video_title, self.video_duration, self.video_author)


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
                         border_width = 1)
        
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
                         border_width = 1)

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
    def __init__(self, parent, video_title, video_duration, video_author):
        super().__init__(master = parent,
                         fg_color = 'transparent',
                         border_width = 1)
        
        self.place(relx = 0,
                   rely = 0.45,
                   relwidth = 1,
                   relheight = 0.35,
                   anchor = 'nw')
        
        VideoInfoLabel(self, 'Title', video_title, 0.15)
        VideoInfoLabel(self, 'Duration', video_duration, 0.35)
        VideoInfoLabel(self, 'Author', video_author, 0.55)
        

class DownloadProgressFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent,
                         fg_color = 'transparent',
                         border_width = 1)
        
        self.place(relx = 0,
                   rely = 0.8,
                   relwidth = 1,
                   relheight = 0.2,
                   anchor = 'nw')