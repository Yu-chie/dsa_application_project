import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
from binary_search_tree_application.bst_main import BSTree
import random

class BSTPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # canvas for binary tree bg 
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)
        
        # load bg image
        self.bg_img = Image.open("assets/bst_bg.png")
        self.bstree_bg = ImageTk.PhotoImage(self.bg_img)
        
        # draw bg 
        self.canvas_bg = self.canvas.create_image(0, 0, image=self.bstree_bg, anchor="nw")
        
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
        
        ''' LOGIC HOLDERS '''
        self.tree = None
        self.n_root = None
        self.values = []
        
        self.user_decision()
        self.traversal_title()
    
    def resize_bg(self, event):
        resized = self.bg_img.resize((event.width, event.height))
        self.btree_bg = ImageTk.PhotoImage(resized)
        
        self.canvas.itemconfig(self.canvas_bg, image=self.btree_bg)
    
    ''' BST METHOD CHOICE '''
    def user_decision(self):
        pass
    
    ''' BST METHOD CONFIRMATION '''
    def confirm_udecision(self):
        pass
    
    ''' FOR USER BST: NODE COUNT INPUT '''
    def user_nodecount_input(self):
        pass
    
    ''' FOR USER BST: NODE COUNT CONFIRMATION '''
    def confirm_nodecount(self):
        pass
    
    ''' USER PROVIDED VALUES FOR BST BUTTONS '''
    def node_user(self):
        pass
    
    ''' DRAWING BSTREE '''
    def generate_bstree(self):
        pass
    
    ''' FOR TRAVERSAL TITLE'''
    def traversal_title(self):
        pass
    
    ''' FOR PRINTING TRAVERSAL '''
    def traversal_holder(self):
        pass
    
    def reset_tree(self):
        pass