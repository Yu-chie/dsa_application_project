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
        
        ''' for scrollable tree canvas '''
        self.tree_frame = tk.Frame(self)
        self.tree_frame.place(x=50, y=120, width=1000, height=600)
        
        self.tree_canvas = tk.Canvas(self.tree_frame, bg="#b6aff0", highlightthickness=0)
        self.tree_canvas.pack(side="left", fill="both", expand=True)
        
        ''' for scrollbar '''
        self.tree_scrollbar = tk.Scrollbar(
            self.tree_frame, orient="vertical", command=self.tree_canvas.yview)
        self.tree_scrollbar.pack(side="right", fill="y")
        
        self.tree_canvas.configure(yscrollcommand=self.tree_scrollbar.set)
        
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
        
        # restart button for all
        self.restartall_button = tk.Button(
            self.canvas, 
            text="Go back to Node Selection",
            font=("VT323", 15),
            bg = "#ecb1ff",
            fg = "#330084",
            activebackground="#330084",
            activeforeground="#ffffff",
            command=self.restart_all
        ) 
        
        self.canvas.create_window(1295, 700, window=self.restartall_button)
        
        # show randomized values
        self.random_label = tk.Label(
            self.canvas,
            text="",
            font=("VT323", 13),
            bg="#b8a8f1",
            wraplength=330,
            justify="left"
        )

        self.canvas.create_window(1295, 150, window=self.random_label)
        
        ''' LOGIC HOLDERS '''
        self.tree = None
        
        self.nodecount_input()
        self.traversal_title()
    
    def resize_bg(self, event):
        resized = self.bg_img.resize((event.width, event.height))
        self.btree_bg = ImageTk.PhotoImage(resized)
        
        self.canvas.itemconfig(self.canvas_bg, image=self.btree_bg)
    
    ''' GENERAL: GO BACK TO NODE SELECTION '''
    def restart_all(self):
        # clear tree and traversal
        self.tree = None
        self.tree_canvas.delete("tree")
        self.inorder_title.config(text="...")
        
        # destroy widgets
        widgets = [
            "asknodes_label", "ncount_entry", "ncount_button",
            "askuser_label", "userinput_button", "randombst_button",
            "value_label", "value_entry", "value_button",
            "reset_button", "regen_button", "random_label"
        ]
        
        for spec in widgets:
            if hasattr(self, spec):
                getattr(self, spec).destroy()
                
        self.nodecount_input()
    
    ''' GENERAL: NODE COUNT INPUT '''
    def nodecount_input(self):
        self.asknodes_label = tk.Label(
            self.canvas,
            text="How many nodes would you like? (10-30)",
            font=("VT323", 19),
            bg = "#b8a8f1"
        )
        
        self.ncount_entry = tk.Entry(
            self.canvas,
            font=("VT323", 20),
            justify="center"
        ) 
        
        self.ncount_button = tk.Button(
            self.canvas,
            text="Confirm Node Count",
            font=("VT323", 15),
            bg = "#ecb1ff",
            fg = "#330084",
            activebackground="#330084",
            activeforeground="#ffffff",
            command=self.confirm_nodecount
        )
        
        self.canvas.create_window(1298, 108, window=self.asknodes_label)
        self.canvas.create_window(1296, 170, window=self.ncount_entry)
        self.canvas.create_window(1295, 230, window=self.ncount_button)
    
    ''' GENERAL: NODE COUNT CONFIRMATION '''
    def confirm_nodecount(self):
        try:
            max_node = int(self.ncount_entry.get())
            
            if not isinstance(max_node, int):
                raise TypeError
            
            if max_node < 10 or max_node > 30:
                raise ValueError
            
            self.tree = BSTree(max_node)
            
        except TypeError:
            self.ncount_entry.delete(0, tk.END)
            messagebox.showerror(
                "Invalid",
                "Nodes must be between 10-30 only"  
            )
            
            return
        
        except ValueError:
            self.ncount_entry.delete(0, tk.END)
            messagebox.showerror(
                "Invalid",
                "Nodes must be between 10-30 only" 
            )
            
            return
        
        self.tree = BSTree(max_node)
        
        self.asknodes_label.destroy()
        self.ncount_entry.destroy()
        self.ncount_button.destroy()
        
        self.user_decision()
    
    ''' GENERAL: METHOD CHOICE '''
    def user_decision(self):
        self.askuser_label = tk.Label(
            self.canvas, 
            text="Generate your Binary Search Tree (BST) using:",
            font=("VT323", 19),
            bg = "#b8a8f1",
            justify="center",
            wraplength=430
        )
        
        self.userinput_button = tk.Button(
            self.canvas,
            text="Self-input values",
            font=("VT323", 15),
            bg = "#ecb1ff",
            fg = "#330084",
            activebackground="#330084",
            activeforeground="#ffffff",
            command=self.nodeval_user
        )
        
        self.randombst_button = tk.Button(
            self.canvas,
            text="Randomized values",
            font=("VT323", 15),
            bg = "#ecb1ff",
            fg = "#330084",
            activebackground="#330084",
            activeforeground="#ffffff",
            command=self.generate_rbst
        )
        
        self.canvas.create_window(1293, 120, window=self.askuser_label)
        self.canvas.create_window(1293, 185, window=self.userinput_button)
        self.canvas.create_window(1293, 235, window=self.randombst_button)
    
    ''' USER: NODE VALUE INPUT '''
    def nodeval_user(self):
        self.askuser_label.destroy()
        self.userinput_button.destroy()
        self.randombst_button.destroy()
        
        self.value_label = tk.Label(
            self.canvas,
            text="Enter your node values:",
            font=("VT323", 19),
            bg = "#b8a8f1"
        )
        
        self.value_entry = tk.Entry(
            self.canvas,
            text="Confirm Tree Level",
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
            command=self.reset_tree
        ) 
        
        self.canvas.create_window(1298, 108, window=self.value_label)
        self.canvas.create_window(1296, 170, window=self.value_entry)
        self.canvas.create_window(1295, 230, window=self.value_button)
        self.canvas.create_window(1295, 640, window=self.reset_button)
    
    ''' USER: ADD NODE VALUES MANUALLY LOGIC '''
    def add_nvalue(self):
        val = self.value_entry.get().strip()
        self.value_entry.delete(0, tk.END)
        
        # for empty inputs
        if val == "":
            messagebox.showerror(
                "Invalid Input",
                "Only enter integer values"
            )
            return
        
        # no empty nodes
        if val == ".":
            messagebox.showerror(
                "Invalid Input",
                "Empty node are not allowed this time. Only enter integer values"
            )
            return
        
        # integer only
        try:
            value  = int(val)
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Only whole numbers (integers) are allowed."
            )
            return
        
        # insert to BST
        try:
            self.tree.ctrl_insert(value)
        except OverflowError:
            messagebox.showerror(
                "Your Binary Search Tree is Full!",
                "You have reached the maximum nodes for your Binary Tree."
            )
            return
        
        self.generate_ubst()
        self.traversal_holder()
    
    ''' USER: DRAWING BSTREE '''
    def generate_ubst(self):
        self.tree_canvas.delete("tree")
        
        def draw_nodes(node, x, y ,r):
            # node drawing control = avoids overlap
            next_r = max(r//2, 30)
            level_y = 100
            
            if node is None:
                return
            
            if node.left:
                self.tree_canvas.create_line(x, y, x-r, y+80, tags="tree")
                draw_nodes(node.left, x-r, y+level_y, next_r)
                
            if node.right:
                self.tree_canvas.create_line(x, y, x+r, y+80, tags="tree")
                draw_nodes(node.right, x+r, y+level_y, next_r)
                
            self.tree_canvas.create_oval(
                x-20, y-20, x+20, y+20, 
                fill="#ecb1ff", outline="#330084", tags="tree")
            
            self.tree_canvas.create_text(
                    x, y, text=node.value, 
                    font=("VT323"), tags="tree")
            
            if self.tree and self.tree.root:
                draw_nodes(self.tree.root, 500, 25, 200)
            
        ''' for scrollbar in tree frame '''
        self.tree_canvas.update_idletasks()
        
        bstbox = self.tree_canvas.bbox("tree")
        if bstbox: 
            x1, y1, x2, y2, = bstbox
            
            canvas_width = self.tree_canvas.winfo_width()
            canvas_height = self.tree_canvas.winfo_height()
            
            # forced top allignment of tree 
            self.tree_canvas.configure(
                scrollregion=(0, 0, max(x2, canvas_width), max(y2, canvas_height))
                )
            
            # view on top
            self.tree_canvas.yview_moveto(0)
        
    ''' USER: RESET PROGRESS '''
    def reset_tree(self):
        # clear tree canvas
        self.tree_canvas.delete("tree")
        
        # reset logic
        if self.tree:
            self.tree.root = None
            self.tree.n_count = 0
            
        # reset traversal
        self.inorder_title.config(text="...")
        
        # clear entry box
        if hasattr(self, "value_entry"):
            self.value_entry.delete(0, tk.END)

    ''' RANDOMIZED: DRAWING BSTREE '''
    def generate_rbst(self):
        self.askuser_label.destroy()
        self.userinput_button.destroy()
        self.randombst_button.destroy()
        
        # button for generate
        self.regen_button = tk.Button(
            self.canvas,
            text="Regenerate Random Binary Search Tree",
            font=("VT323", 15),
            bg = "#ecb1ff",
            fg = "#330084",
            activebackground="#330084",
            activeforeground="#ffffff",
            command=self.regenerate_rbst
        )
        
        self.canvas.create_window(1295, 230, window=self.regen_button)
    
        # rbst gui logic
        self.tree_canvas.delete("tree")
        self.logic_rbst()
        
        # show randomized value
        values_str = ", ".join(map(str, self.random_values))
        self.random_label.config(text=f"Generated Values:\n{values_str}")
        
        # draw and give traversal
        self.generate_ubst()
        self.traversal_holder()
        
    ''' RANDOMIZED: DRAWING BSTREE LOGIC '''
    def logic_rbst(self):
        # reset root just in case
        self.tree.root = None
        self.tree.n_count = 0
        
        # reset values
        self.random_values = []
                
        try:
            for _ in range(self.tree.max_node):
                value = random.randint(1,100)
                self.random_values.append(value)
                self.tree.ctrl_insert(value)
        except OverflowError:
            pass
        
    ''' RANDOMIZED: REGENERATE RBST '''
    def regenerate_rbst(self):
        self.tree_canvas.delete("tree")
        
        self.logic_rbst()
        
        # show randomized value
        values_str = ", ".join(map(str, self.random_values))
        self.random_label.config(text=f"Generated Values:\n{values_str}")
        
        self.generate_ubst()
        self.traversal_holder()
    
    ''' GENERAL: TRAVERSAL TITLE'''
    def traversal_title(self):
        self.inorder_title = tk.Label(
            self.canvas, 
            text="...",
            font=("VT323", 15),
            bg = "#9d8cf3",
            wraplength=330,
            justify="left"
        )
        
        self.canvas.create_window(1290, 455, window=self.inorder_title)
    
    ''' GENERAL: PRINTING TRAVERSAL '''
    def traversal_holder(self):
        if not self.tree or not self.tree.root:
            return
        
        ltr_list = self.tree.trav_inorder(self.tree.root)
        ltr = " ".join(map(str, ltr_list))
        
        self.inorder_title.config(text=ltr, bg="#9d8cf3")
    