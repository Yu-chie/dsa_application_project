import tkinter as tk
from PIL import Image, ImageTk

class QueueGUI:
    def __init__(self, garage):
        self.garage = garage
        
        self.root = tk.Tk()
        self.root.title("Queue Parking Garage Simulator")
        self.root.geometry("800x500")
        self.root.resizable(False, False)
        
        # Load and set background image
        self.bg_image = Image.open("queue_application/queue_gui/queue_bg.png")
        self.bg_image = self.bg_image.resize((800, 500))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        self.canvas = tk.Canvas(self.root, width=800, height=500)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
    
    def run(self):
        self.root.mainloop()