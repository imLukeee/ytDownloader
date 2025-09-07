import customtkinter as ctk
from settings import *

class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color = "#353434")

        #center window on screen
        width = self.winfo_screenwidth()
        height = self.winfo_screenheight()
        x = width // 2 - (APP_SIZE[0] //2)
        y = height // 2 - (APP_SIZE[1] // 2)

        #general window setup
        self.title(TITLE)
        self.geometry(f'{APP_SIZE[0]}x{APP_SIZE[1]}+{x}+{y}')

    
        self.mainloop()