import customtkinter as ctk
from settings import *

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

        #widgets
        self.create_widgets()

        self.mainloop()

    def create_widgets(self):
        self.Title = TitleLabel(self)
        self.UrlFrame = UrlFrame(self)
        self.OptionButtonsFrame = OptionButtonsFrame(self)


class TitleLabel(ctk.CTkLabel):
    def __init__(self, parent):
        super().__init__(master = parent,
                       text = 'YT Downloader',
                       font = ctk.CTkFont('JetBrains Mono', 64, 'bold'))

        self.place(relx = 0.5,
                   rely = 0.05,
                   relwidth = 1,
                   relheight = 0.1,
                   anchor = 'center',)

    
class UrlFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent,
                         fg_color = 'transparent',
                         border_width = 1)
        
        self.widget_font = ctk.CTkFont('JetBrains Mono', 32, 'normal')

        self.place(relx = 0,
                   rely = 0.15,
                   relwidth = 1,
                   relheight = 0.2,
                   anchor = 'nw')
        
        self.instruction = ctk.CTkLabel(self,
                                        font = self.widget_font,
                                        text = 'Insert a valid URL')
        
        self.url_entry = ctk.CTkEntry(self,
                                      font = self.widget_font,
                                      corner_radius = 12)
        
        self.instruction.place(relx = 0.5,
                               rely = 0.2,
                               relheight = 0.2,
                               relwidth = 1,
                               anchor = 'center')
        
        self.url_entry.place(relx = 0.5,
                             rely = 0.6,
                             relwidth = 0.6,
                             relheight = 0.4,
                             anchor = 'center')
        

class OptionButtonsFrame(ctk.CTkFrame):
    def __init__(self, parent):
        super().__init__(master = parent,
                         fg_color = 'transparent',
                         border_width = 1)

        self.place(relx = 0,
                   rely = 0.35,
                   relwidth = 1,
                   relheight = 0.15,
                   anchor = 'nw')