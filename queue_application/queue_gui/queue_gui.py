import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk

class QueueGUI:
    def __init__(self, garage):
        self.garage = garage
        
        self.root = tk.Tk()
        self.root.title("Queue Parking Garage Simulator")
        self.root.geometry("800x500")
        self.root.resizable(False, False)
        
        # Background image
        self.bg_image = Image.open("queue_application/queue_gui/queue_bg.png")
        self.bg_image = self.bg_image.resize((800, 500))
        self.bg_photo = ImageTk.PhotoImage(self.bg_image)
        
        self.canvas = tk.Canvas(self.root, width=800, height=500)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        
        # Buttons
        self.arrive_btn = tk.Button(
            self.root,
            text="Car Arrives",
            font=("VT323", 16),
            width=15,
            command=self.car_arrives
        )
        
        self.depart_btn = tk.Button(
            self.root,
            text="Car Departs",
            font=("VT323", 16),
            width=15,
            command=self.car_departs
        )
        
        self.exit_btn = tk.Button(
            self.root,
            text="Exit",
            font=("VT323", 16),
            width=15,
            command=self.root.quit
        )
        
        self.canvas.create_window(200, 400, window=self.arrive_btn)
        self.canvas.create_window(400, 400, window=self.depart_btn)
        self.canvas.create_window(600, 400, window=self.exit_btn)
        
    def car_arrives(self):
        plate = simpledialog.askstring("Car Arrives", "Enter the car's plate number:")
        if not plate:
            return
        result = self.garage.car_arrives(plate)
        messagebox.showinfo("Car Arrives", result)
        self.draw_table()
    
    def car_departs(self):
        plate = simpledialog.askstring("Car Departs", "Enter the car's plate number:")
        if not plate:
            return
        result = self.garage.car_departs(plate)
        messagebox.showinfo("Car Departs", result)
        self.draw_table()

    def draw_table(self):
        self.canvas.delete("table")
        
        y = 80
        headers = ["Slot", "Plate Number", "# of Arrivals", "# of Departures"]
        
        for i, header in enumerate(headers):
            self.canvas.create_text(
                150 + i*150, y, 
                text=header, 
                font=("VT323", 14, "bold"), 
                tags="table"
            )
            
        y += 30
        
        for i, car in enumerate(self.garage.queue):
            if car is None:
                values = [i+1, "-", "-", "-"]
            else:
                values = [
                    i + 1,
                    car['plate_number'],
                    car['arrival_count'],
                    car['departure_count']
                ]
            
            for j, value in enumerate(values):
                self.canvas.create_text(
                    150 + j*150, y, 
                    text=value, 
                    font=("VT323", 12), 
                    tags="table"
                )
            
            y += 25
    
    def run(self):
        self.draw_table()  # Draw table on GUI start
        self.root.mainloop()
