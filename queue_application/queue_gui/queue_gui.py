import tkinter as tk

class QueueGUI:
    def __init__(self, garage):
        self.garage = garage
        
        self.root = tk.Tk()
        self.root.title("Queue Parking Garage Simulator")
        self.root.geometry("800x500")
        self.root.resizable(False, False)
    
    def run(self):
        self.root.mainloop()