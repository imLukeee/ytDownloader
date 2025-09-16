import customtkinter as ctk
from settings import *
from PIL import Image, ImageTk
import requests
from io import BytesIO


class OptionSelector(ctk.CTkSegmentedButton):
    def __init__(self, parent, values, variable, relx):
        super().__init__(master = parent,
                         text_color = INPUT_FIELD_COLOR,
                         font = ctk.CTkFont(*BUTTON_FONT_DATA),
                         values = values,
                         variable = variable,
                         corner_radius = 12)
        
        self.place(relx = relx,
                   rely = 0.5,
                   relheight = 0.6,
                   relwidth = 0.2,
                   anchor = 'w')
        

class DownloadButton(ctk.CTkButton):
    def __init__(self, parent, command):
        super().__init__(master = parent,
                         text = 'Download',
                         text_color = INPUT_FIELD_COLOR,
                         font = ctk.CTkFont(*BUTTON_FONT_DATA),
                         command = command,
                         corner_radius = 12,
                         fg_color = '#7BBBD2',
                         hover_color = "#54ACCD")
        
        self.place(relx = 0.65,
                   rely = 0.5,
                   relheight = 0.6,
                   relwidth = 0.2,
                   anchor = 'w')
    

class VideoInfoLabel(ctk.CTkLabel):
    def __init__(self, parent, label_key, label_value, rely):
        super().__init__(master = parent,
                         text = f'{label_key}:\n{label_value}',
                         font = ctk.CTkFont(*BUTTON_FONT_DATA),
                         text_color = FONT_COLOR)
        
        self.place(relx = 0.5,
                   rely = rely,
                   anchor = 'center')
        

class DownloadProgressBar(ctk.CTkProgressBar):
    def __init__(self, parent, percent_var):
        super().__init__(master = parent,
                         orientation = 'horizontal',
                         variable = percent_var,
                         progress_color = "#08ca1e"
                         )
        
        self.place(relx = 0.5,
                   rely = 0.5,
                   relwidth = 0.8,
                   anchor = 'center')
        

class ThumbnailPreview(ctk.CTkCanvas):
    def __init__(self, parent, thumbnail_url):
        super().__init__(master = parent, 
                         bg = 'white',
                         bd=0,
                         relief='ridge'
                        )

        self.place (relx = 0.5,
                    rely = 0.25,
                    relwidth = 0.25,
                    relheight = 0.4,
                    anchor = 'center')

        self.image = self.fetch_image_from_url(thumbnail_url)

        self.bind('<Configure>', lambda event: self.resize_image(event))

    
    def fetch_image_from_url(self, url):
        response = requests.get(url)
        response.raise_for_status()
        img_data = BytesIO(response.content)

        return Image.open(img_data).convert('RGBA')
    

    def resize_image(self, event_data):
        image_ratio = self.image.width / self.image.height
        canvas_ratio = event_data.width / event_data.height

        if image_ratio < canvas_ratio:
            self.img_height = event_data.height
            self.img_width = int(self.img_height * image_ratio)
        elif image_ratio > canvas_ratio:
            self.img_width = event_data.width
            self.img_height = int(self.img_width / image_ratio)

        self.place_image(event_data)

    def place_image(self, event_data):
        resized = self.image.resize((self.img_width, self.img_height))
        self.imagetk = ImageTk.PhotoImage(resized)

        self.center_width = (event_data.width - self.img_width) / 2
        self.center_height = (event_data.height - self.img_height) / 2

        self.delete('all')
        self.create_image(self.center_width, self.center_height, anchor = 'nw', image = self.imagetk)