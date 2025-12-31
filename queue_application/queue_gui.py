import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
from queue_application.parking_garage import ParkingGarage

class QueueGUI(tk.Frame):
    def __init__(self, parent, garage):
        super().__init__(parent)
        self.garage = garage
        
        # Canvas setup
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.resize_bg)
        
        # Background image
        self.bg_image = Image.open("queue_application/queue_gui/queue_bg.png")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image.resize((1920, 1080)))
        self.bg_image_id = self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        
        # Buttons
        self.arrive_btn = tk.Button(
            self,
            text="Car Arrives",
            font=("VT323", 16),
            width=15,
            command=self.car_arrives
        )
        
        self.depart_btn = tk.Button(
            self,
            text="Car Departs",
            font=("VT323", 16),
            width=15,
            command=self.car_departs
        )
        
        self.exit_btn = tk.Button(
            self,
            text="Exit",
            font=("VT323", 16),
            width=15,
            command=self.destroy
        )
        
        # Place buttons initially (will be repositioned on resize)
        self.arrive_btn_window = self.canvas.create_window(1550, 250, window=self.arrive_btn)
        self.depart_btn_window = self.canvas.create_window(1550, 350, window=self.depart_btn)
        self.exit_btn_window = self.canvas.create_window(1550, 450, window=self.exit_btn)

        
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
        
    def resize_bg(self, event):
        # Resize background
        resized_bg = self.bg_image.resize((event.width, event.height))
        self.bg_photo = ImageTk.PhotoImage(resized_bg)
        self.canvas.itemconfig(self.bg_image_id, image=self.bg_photo)
        
        # Reposition buttons in upper-right box
        self.canvas.coords(self.arrive_btn_window, event.width - 400, 250)
        self.canvas.coords(self.depart_btn_window, event.width - 400, 350)
        self.canvas.coords(self.exit_btn_window, event.width - 400, 450)