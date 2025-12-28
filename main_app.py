import tkinter as tk
from PIL import Image, ImageTk

class MainApp(tk.Tk):
    def __init__(self):
        super().__init()       # initialize tk and set this as parent class
        
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
    pass

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