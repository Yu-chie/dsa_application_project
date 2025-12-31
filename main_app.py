import tkinter as tk
from PIL import Image, ImageTk

# QUEUE
from queue_application.parking_garage import ParkingGarage
from queue_application.file_manager import FileManager
from queue_application.queue_gui import QueueGUI

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()       # initialize tk
        
        # general window title, dimension, and allow fullscreen
        self.title("DSA App")
        self.geometry("1920x1080")
        self.resizable(True, True)
        
        # for holding pages as frames (allow smooth change of windows)
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)
        
        self.frames = {}
        # list of pages included (so if may dinedevelop na page i-add ung class dito para magpakita pag ni-run)
        for page in (StartPage, SelectPage, DevPage, StackPage, QueuePage, BTPage, BSTPage):  
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
        
        self.canvas.create_window(450, 500, window=play_button)     # will create the button window (450, 500) is x and y position
        
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
    def __init__(self, parent, controller):
        super().__init__(parent)                 # will be called to parent class
        
        ''' FOR BACKGROUND SETUP '''
        # canvas for storing the background of start page
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)
        
        # load the background image in canvas
        self.bg_img = Image.open("assets/select_bg.png")
        self.select_bg = ImageTk.PhotoImage(self.bg_img)
        
        # draw bg  
        self.canvas_bg = self.canvas.create_image(0, 0, image=self.select_bg, anchor="nw")
        
        # auto resize of background
        self.canvas.bind("<Configure>", self.resize_bg)  
        
        ''' FOR BUTTONS AND LABELS '''
        # home button to go back to home
        home_button = tk.Button(
            self,
            text="HOME",
            font=("VT323", 12),
            bg = "#594faf",
            fg = "#ffffff",
            activebackground="#330084",
            activeforeground="#ffffff",
            padx=65,
            command=lambda: controller.show_frame("StartPage")
        )
        
        self.canvas.create_window(103, 38, window=home_button) 
        
        # stack button to direct to stack garage page
        stack_button = tk.Button(
            self,
            text="STACK",
            font=("VT323", 20),
            bg = "#ecb1ff",
            fg = "#330084",
            activebackground="#330084",
            activeforeground="#ffffff",
            padx=73,
            command=lambda: controller.show_frame("StackPage")
        )
        
        self.canvas.create_window(300, 400, window=stack_button)
        
        # queue button to direct to queue garage page
        queue_button = tk.Button(
            self,
            text="QUEUE",
            font=("VT323", 20),
            bg = "#ecb1ff",
            fg = "#330084",
            activebackground="#330084",
            activeforeground="#ffffff",
            padx=70,
            command=lambda: controller.show_frame("QueuePage")
        )
        
        self.canvas.create_window(1250, 400, window=queue_button)
        
        # bt button to direct to binary tree page
        bt_button = tk.Button(
            self,
            text="BINARY TREE",
            font=("VT323", 20),
            bg = "#ecb1ff",
            fg = "#330084",
            activebackground="#330084",
            activeforeground="#ffffff",
            padx=60,
            command=lambda: controller.show_frame("BTPage")
        )
        
        self.canvas.create_window(773, 520, window=bt_button)
        
        # bst button to direct to binary search tree page
        bst_button = tk.Button(
            self,
            text="BINARY SEARCH TREE",
            font=("VT323", 20),
            bg = "#ecb1ff",
            fg = "#330084",
            activebackground="#330084",
            activeforeground="#ffffff",
            padx=3,
            command=lambda: controller.show_frame("BSTPage")
        )
        
        self.canvas.create_window(300, 650, window=bst_button)
        
        # recursion button to direct to hanoi page
        hanoi_button = tk.Button(
            self,
            text="RECURSION",
            font=("VT323", 20),
            bg = "#ecb1ff",
            fg = "#330084",
            activebackground="#330084",
            activeforeground="#ffffff",
            padx=50,
            command=lambda: controller.show_frame("HanoiPage")
        )
        
        self.canvas.create_window(1250, 646, window=hanoi_button)
        
    def resize_bg(self, event):
        resized = self.bg_img.resize((event.width, event.height))
        self.select_bg = ImageTk.PhotoImage(resized)
        
        self.canvas.itemconfig(self.canvas_bg, image=self.select_bg)

class StackPage(tk.Frame):
    pass

class QueuePage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        # File Manager setup
        file_manager = FileManager()
        
        # Parking Garage Logic
        garage = ParkingGarage(file_manager=file_manager)
        
        # GUI setup
        queue_gui = QueueGUI(self, garage)
        queue_gui.pack(fill="both", expand=True)
        
        # Home Button
        home_button = tk.Button(
            self,
            text="HOME",
            font=("VT323", 12),
            bg = "#594faf",
            fg = "#ffffff",
            padx=65,
            command=lambda: controller.show_frame("StartPage")
        )
        home_button.place(x=30, y=30)

class BTPage(tk.Frame):
    pass

class BSTPage(tk.Frame):
    pass

class DevPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        
        ''' FOR BACKGROUND SETUP '''
        # canvas for storing the background of start page
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)
        
        # load the background image in canvas
        self.bg_img = Image.open("assets/test_dev_bg.png")
        self.dev_bg = ImageTk.PhotoImage(self.bg_img)
        
        # draw bg 
        self.canvas_bg = self.canvas.create_image(0, 0, image=self.dev_bg, anchor="nw")
        
        # auto resize of background
        self.canvas.bind("<Configure>", self.resize_bg)   
        
        '''FOR BUTTONS AND LABELS'''
        # home button to go back to home
        home_button = tk.Button(
            self,
            text="HOME",
            font=("VT323", 12),
            bg = "#594faf",
            fg = "#ffffff",
            activebackground="#330084",
            activeforeground="#ffffff",
            padx=65,
            command=lambda: controller.show_frame("StartPage")
        )
        
        self.canvas.create_window(103, 38, window=home_button)
        
    def resize_bg(self, event):
        resized = self.bg_img.resize((event.width, event.height))
        self.dev_bg = ImageTk.PhotoImage(resized)
        
        self.canvas.itemconfig(self.canvas_bg, image=self.dev_bg)


if __name__ == "__main__":
    run_app = MainApp()
    run_app.mainloop()