import tkinter as tk
from PIL import Image, ImageTk

class MainApp(tk.Tk):
    def __init__(self):
        super().__init()       # initialize tk
        
        # general window title, dimension, and allow fullscreen
        self.title("DSA App")
        self.geometry("1920x1080")
        self.resizable(True, True)
        
        # for holding pages as frames (allow smooth change of windows)
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        
        self.frames = {}
        # list of pages included (so if may dinedevelop na page i-add ung class dito para magpakita pag ni-run)
        for page in (StartPage, SelectPage, DevPage):  
            frame = page(container, self)
            self.frames[page.__name__] = frame
            frame.place(relwidth=1, relheight=1)
            
        self.show_frame("StartPage")   # first page shown will be the Start Page
    
    def show_frame(self, page_name):
        self.frames[page_name].tkraise()

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)                # start page is the parent class
        self.controller = controller
        
        ''' FOR BACKGROUND SETUP '''
        # canvas for storing the background of start page
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)
        
        # load the background image in canvas
        self.bg_img = Image.open("assets/test_main_bg.png")
        self.start_bg = ImageTk.PhotoImage(self.bg_img)
        
        # draw bg
        self.canvas_bg = self.canvas.create_image(0, 0, image=self.start_bg, anchor="nw")
        
        # auto resize of background
        self.canvas.bind("<Configure>", self.resize_bg)
        
        ''' FOR BUTTONS AND LABELS '''
        # play button to direct to select page
        play_button = tk.Button(
            self,
            text="PLAY",                     # text display
            font=("VT323", 20),              # font name, size 
            bg = "#ecb1ff",                # bg color 
            fg = "#330084",                # font color
            activebackground="#330084",    # bg color upon click
            activeforeground="#ffffff",    # font color upon click
            padx=85,                         # width of button alone 
            command=lambda: controller.show_frame("SelectPage")            # will direct to select page upon click
        )
        
        # dev button to direct to dev page
        dev_button = tk.Button(
            self,
            text="MEET THE DEVS",
            font=("VT323", 20),
            bg = "#ecb1ff",
            fg = "#330084",
            activebackground="#330084",
            activeforeground="#ffffff",
            padx=36,
            command=lambda: controller.show_frame("DevPage")             # will direct to dev page upon click
        )
        self.canvas.create_window(450, 570, window=dev_button)
        
    def resize_bg(self, event):
        resized = self.bg_img.resize((event.width, event.height))
        self.start_bg = ImageTk.PhotoImage(resized)
        
        self.canvas.itemconfig(self.canvas_bg, image=self.start_bg)
    

class SelectPage(tk.Frame):
    pass

class StackPage(tk.Frame):
    pass

class QueuePage(tk.Frame):
    pass

class BTPage(tk.Frame):
    pass

class BSTPage(tk.Frame):
    pass

class DevPage(tk.Frame):
    pass


if __name__ == "__main__":
    run_app = MainApp()
    run_app.mainloop()