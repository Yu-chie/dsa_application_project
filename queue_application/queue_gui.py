import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
from queue_application.parking_garage import ParkingGarage
import random 

class QueueGUI(tk.Frame):
    def __init__(self, parent, garage):
        super().__init__(parent)
        self.garage = garage
        self.running = True
        
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
        
        if self.garage.mode == "AUTO":
            self.arrive_btn.config(state="disabled")
            self.depart_btn.config(state="disabled")
        
        # Game loop
        if self.garage.mode == "AUTO":
            self.auto_arrival()
            self.auto_depart()
        elif self.garage.mode == "MANUAL":
            pass  # slower arrivals
        
        self.draw_table()
        self.draw_waiting_area()                
        self.update_waiting_timers()

        
    def car_arrives(self):
        if not self.garage.waiting:
            messagebox.showinfo("Info", "No cars waiting")
            return
        
        car = self.garage.waiting.pop(0)
        result = self.garage.car_arrives(car["plate_number"])
        messagebox.showinfo("Car Arrives", result)
        self.draw_table()
        self.draw_waiting_area()
    
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

        self.draw_waiting_area()
        
    def auto_arrival(self):
        if not self.running:
            return

        plate = f"CAR-{random.randint(100,999)}"
        result = self.garage.add_to_waiting(plate)
        if result == "Waiting Area Full":
            messagebox.showwarning("Waiting Area", "Waiting Area is Full!")

        self.draw_table()

        self.after(3000, self.auto_arrival)  # every 3 seconds
        self.draw_waiting_area()

    def auto_depart(self):
        if not self.running or self.garage.mode != "AUTO":
            return

        for car in self.garage.queue:
            if car:
                self.garage.car_departs(car['plate_number'])
                break

        self.draw_table()
        self.after(5000, self.auto_depart)

    def draw_waiting_area(self):
        self.canvas.delete("waiting")
        
        y = 600
        self.canvas.create_text(
            300, y,
            text="WAITING AREA",
            font=("VT323", 18, "bold"),
            tags="waiting"
        )

        y += 30
        for car in self.garage.waiting:
            self.canvas.create_text(
                300, y,
                text=f"{car['plate_number']} | Time left: {car['time_left']}",
                font=("VT323", 14),
                tags="waiting"
            )
            y += 25 
            
    def update_waiting_timers(self):
        expired = []

        for car in self.garage.waiting:
            car["time_left"] -= 1
            if car["time_left"] <= 0:
                expired.append(car)

        for car in expired:
            self.garage.waiting.remove(car)
            messagebox.showwarning(
                "Game Warning",
                f"Car {car['plate_number']} waited too long!"
            )
            self.garage.failed_cars += 1

        self.draw_waiting_area()
        self.after(1000, self.update_waiting_timers)

    def stop(self):
        self.running = False
        self.destroy()