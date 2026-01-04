import tkinter as tk 
from tkinter import messagebox
from PIL import Image, ImageTk
from binary_tree_application.bt_main import Tree

class BTPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # canvas for binary tree bg 
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)
        
        # load bg image
        self.bg_img = Image.open("assets/bt_bg.png")
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
        self.traversal_title()
        
    def resize_bg(self, event):
        resized = self.bg_img.resize((event.width, event.height))
        self.btree_bg = ImageTk.PhotoImage(resized)
        
        self.canvas.itemconfig(self.canvas_bg, image=self.btree_bg)
    
    ''' FOR TREE LEVEL INPUT '''
    def treelvl_input(self):
        self.inputlvl_label = tk.Label(
            self.canvas,
            text="Enter your Binary Tree Level (1-5):",
            font=("VT323", 19),
            bg = "#b8a8f1"
        )
        
        self.treelvl_entry = tk.Entry(
            self.canvas,
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
    
    ''' TREE LEVEL CONFIRMATION - with error handling'''
    def confirm_treelvl(self):
        try:
            levels = int(self.treelvl_entry.get())
            self.treelvl_entry.delete(0, tk.END)
            
            if not isinstance(levels, int):
                raise TypeError
            
            if levels < 1 or levels > 5:
                raise ValueError
            
            self.tree = Tree(levels)
            
        except TypeError:
            self.treelvl_entry.delete(0, tk.END)
            messagebox.showerror(
                "Invalid",
                "Tree level must be between 1-5 only"  
            )
            
            return
        
        except ValueError:
            self.treelvl_entry.delete(0, tk.END)
            messagebox.showerror(
                "Invalid", 
                "Tree level must be between 1-5 only"
            )
            
            return
        
        self.tree = Tree(levels)
        
        self.inputlvl_label.destroy()
        self.treelvl_entry.destroy()
        self.treelvl_button.destroy()
        
        self.value_input()
    
    ''' FOR VALUE ENTRIES IN TREE '''
    def value_input(self):
        self.value_label = tk.Label(
            self.canvas,
            text="Enter your node values:",
            font=("VT323", 19),
            bg = "#b8a8f1"
        )
        
        self.note_label = tk.Label(
            self.canvas,
            text="Enter a period (.) or leave it blank for empty nodes",
            font=("VT323", 11),
            bg = "#b8a8f1",
            fg= "#59007a"
        )
        
        self.value_entry = tk.Entry(
            self.canvas,
            font=("VT323", 20),
            justify="center"
        )
        
        self.value_button = tk.Button(
            self.canvas,
            text="Submit",
            font=("VT323", 15),
            bg = "#ecb1ff",
            fg = "#330084",
            activebackground="#330084",
            activeforeground="#ffffff",
            command=self.add_nvalue
        )
        
        self.reset_button = tk.Button(
            self.canvas, 
            text="Reset Progress",
            font=("VT323", 15),
            bg = "#ecb1ff",
            fg = "#330084",
            activebackground="#330084",
            activeforeground="#ffffff",
            command=self.reset_progress
        )
        
        self.canvas.create_window(1298, 108, window=self.value_label)
        self.canvas.create_window(1298, 135, window=self.note_label)
        self.canvas.create_window(1296, 170, window=self.value_entry)
        self.canvas.create_window(1295, 230, window=self.value_button)
        self.canvas.create_window(1295, 640, window=self.reset_button)
        
    ''' FOR ADDING NODE VALUES '''
    def add_nvalue(self):
        value = self.value_entry.get()
        self.value_entry.delete(0, tk.END)
             
        try: 
            self.tree.insert_node(value)
        except OverflowError:
            messagebox.showerror(
                "Your Binary Tree is Full!",
                "You have reached the maximum nodes for your Binary Tree"
            )
            return
        
        self.generate_tree()
        
        if not self.tree.valid_queue:
            self.traversal_holder()
        
    ''' FOR DRAWING THE TREE '''
    def generate_tree(self):
        self.canvas.delete("tree")
        
        def draw_nodes(n_count, x, y, r):
            if n_count >= len(self.tree.node):
                return
            
            node = self.tree.node[n_count]
            if node is None:
                return
            
            if node.empty_node:
                return
            
            n_left = 2 * n_count + 1
            n_right = 2 * n_count + 2
            
            if (
                n_left < len(self.tree.node) 
                and self.tree.node[n_left] is not None
                and not self.tree.node[n_left].empty_node
            ):
                self.canvas.create_line(x, y, x-r, y+80-20, tags="tree")
                draw_nodes(n_left, x-r, y+80, r//2)

            if (
                n_right < len(self.tree.node) 
                and self.tree.node[n_right] is not None
                and not self.tree.node[n_right].empty_node
            ):
                self.canvas.create_line(x, y, x+r, y+80-20, tags="tree")
                draw_nodes(n_right, x+r, y+80, r//2)
            
            self.canvas.create_oval(
                x-20, y-20, x+20, y+20, 
                fill="#ecb1ff", outline="#330084", tags="tree")
            
            self.canvas.create_text(
                x, y, text=node.value, 
                font=("VT323"), tags="tree")
                
        draw_nodes(0, 500, 200, 200)
        
    ''' FOR TRAVERSAL TITLES '''    
    def traversal_title(self):
        self.preorder_title = tk.Label(
            self.canvas, 
            text="Preorder (TLR): ",
            font=("VT323", 15),
            bg = "#9d8cf3",
            wraplength=330,
            justify="left"
        )
        
        self.inorder_title = tk.Label(
            self.canvas, 
            text="Inorder (LTR): ",
            font=("VT323", 15),
            bg = "#9d8cf3",
            wraplength=330,
            justify="left"
        )
        
        self.postorder_title = tk.Label(
            self.canvas, 
            text="Postorder (LRT): ",
            font=("VT323", 15),
            bg = "#9d8cf3",
            wraplength=330,
            justify="left"
        )
        
        self.canvas.create_window(1290, 362, window=self.preorder_title)
        self.canvas.create_window(1290, 455, window=self.inorder_title)
        self.canvas.create_window(1290, 551, window=self.postorder_title)
        
    ''' FOR PRINTING TRAVERSALS '''
    def traversal_holder(self):
        tlr = " ".join(self.tree.trav_preorder())
        ltr = " ".join(self.tree.trav_inorder())  
        lrt = " ".join(self.tree.trav_postorder())
        
        self.preorder_title.config(text=f"Preorder (TLR): {tlr}", bg="#9d8cf3")
        self.inorder_title.config(text=f"Inorder (LTR): {ltr}", bg="#9d8cf3")
        self.postorder_title.config(text=f"Postorder (LRT): {lrt}", bg="#9d8cf3")
    
    ''' FOR RESETTING PROGRESS '''
    def reset_progress(self):
        # delete tree
        self.canvas.delete("tree")  
        
        # reset tree data
        self.tree = None
        
        # delete traversal
        self.preorder_title.config(text=f"Preorder (TLR):", bg="#9d8cf3")
        self.inorder_title.config(text=f"Inorder (LTR):", bg="#9d8cf3")
        self.postorder_title.config(text=f"Postrder (LRT):", bg="#9d8cf3")
        
        # reset widgets
        self.value_label.destroy()
        self.note_label.destroy()
        self.value_entry.destroy()
        self.value_button.destroy()
        self.reset_button.destroy()

        # revert to tree level inputs
        self.treelvl_input()
