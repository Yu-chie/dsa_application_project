import tkinter as tk 
from tkinter import messagebox
from PIL import Image, ImageTk
from bt_main import Tree

class BTPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # canvas for binary tree bg 
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)
        
        # load bg image
        self.bg_img = Image.open("pics/bt_bg.png")
        self.btree_bg = ImageTk.PhotoImage(self.bg_img)
        
        # draw bg 
        self.canvas_bg = self.canvas.create_image(0, 0, image=self.btree_bg, anchor="nw")
        
        # auto resizing bg 
        self.canvas.bind("<Configure>", self.resize_bg)
        
        # to home button
        home_button = tk.Button(
            self,
            text="HOME",
            font=("VT323", 12),
            bg = "#594faf",
            fg = "#ffffff",
            activebackground="#330084",
            activeforeground="#ffffff",
            padx=65,
            pady=7,
            command=lambda: controller.show_frame("StartPage")
        )
        
        self.canvas.create_window(103, 45, window=home_button)
        
        '''  LOGIC HOLDERS  '''
        self.tree = None
        self.n_root = None
        self.values = []
        
        self.treelvl_input()
        
    def resize_bg(self, event):
        resized = self.bg_img.resize((event.width, event.height))
        self.btree_bg = ImageTk.PhotoImage(resized)
        
        self.canvas.itemconfig(self.canvas_bg, image=self.btree_bg)
    
    ''' FOR TREE LEVEL INPUT '''
    def treelvl_input(self):
        self.inputlvl_label = tk.Label(
            self.canvas,
            text="Enter your Binary Tree Level:",
            font=("VT323", 19),
            bg = "#b8a8f1"
        )
        
        self.treelvl_entry = tk.Entry(
            self.canvas,
            text="Confirm Tree Level",
            font=("VT323", 20),
            justify="center"
        ) 
        
        self.treelvl_button = tk.Button(
            self.canvas,
            text="Confirm Tree Level",
            font=("VT323", 15),
            bg = "#ecb1ff",
            fg = "#330084",
            activebackground="#330084",
            activeforeground="#ffffff",
            command=self.confirm_treelvl
        )
        
        self.canvas.create_window(1298, 108, window=self.inputlvl_label)
        self.canvas.create_window(1296, 170, window=self.treelvl_entry)
        self.canvas.create_window(1295, 230, window=self.treelvl_button)