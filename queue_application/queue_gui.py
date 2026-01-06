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
        self.tick()                

        
    def car_arrives(self):
        if self.garage.game_over:
            return
        
        if not self.garage.waiting:
            messagebox.showinfo("Info", "No cars waiting")
            return
        
        car = self.garage.waiting.pop(0)
        result = self.garage.car_arrives(car["plate_number"])
        messagebox.showinfo("Car Arrives", result)
        self.draw_table()
        self.draw_waiting_area()
        self.draw_stats()
    
    def car_departs(self):
        if self.garage.game_over:
            return
        
        plate = simpledialog.askstring("Car Departs", "Enter the car's plate number:")
        if not plate:
            return
        result = self.garage.car_departs(plate)
        messagebox.showinfo("Car Departs", result)
        self.draw_table()
        self.draw_stats()

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
        
        if result == "Waiting Area Full" and self.garage.mode == "MANUAL":
            messagebox.showwarning("Waiting Area", "Waiting Area is Full!")

        self.draw_waiting_area()
        self.after(3000, self.auto_arrival)  # every 3 seconds
        self.draw_stats()

    def auto_depart(self):
        if not self.running or self.garage.mode != "AUTO":
            return

        for car in self.garage.queue:
            if car:
                self.garage.car_departs(car['plate_number'])
                break

        self.draw_table()
        self.draw_stats()
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
            color = "red" if car["time_left"] <= 2 else "white"
            
            self.canvas.create_text(
                300, y,
                text=f"{car['plate_number']} | Time left: {car['time_left']}",
                font=("VT323", 14),
                fill = color,
                tags="waiting"
            )
            y += 25 
            
        y += 30
        self.canvas.create_text(
            300, y,
            text=f"FAILED CARS: {self.garage.failed_cars}",
            font=("VT323", 16, "bold"),
            fill="red",
            tags="waiting"
        )

    def stop(self):
        self.running = False
        self.destroy()
        
    def tick(self):
        if not self.running:
            return
        
        if self.garage.game_over:
            messagebox.showerror(
                "GAME OVER",
                f"Too many cars failed!\nFinal Score: {self.garage.score}"
            )
            self.stop()
            return

        expired = self.garage.update_waiting()

        for car in expired:
            messagebox.showwarning(
                "Waiting Timeout",
                f"Car {car['plate_number']} waited too long and left!"
            )

        self.draw_waiting_area()
        self.after(1000, self.tick)

    def draw_stats(self):
        self.canvas.delete("stats")

        stats = self.garage.get_stats()

        y = 900
        self.canvas.create_text(
            300, y,
            text=f"TOTAL ARRIVALS: {stats['total_arrivals']}",
            font=("VT323", 14),
            tags="stats"
        )

        self.canvas.create_text(
            300, y + 25,
            text=f"TOTAL DEPARTURES: {stats['total_departures']}",
            font=("VT323", 14),
            tags="stats"
        )
        
        self.canvas.create_text(
            300, y + 50,
            text=f"SCORE: {stats['score']}",
            font=("VT323", 16, "bold"),
            fill="yellow",
            tags="stats"
        )

        self.canvas.create_text(
            300, y + 75,
            text=f"FAILED CARS: {stats['failed_cars']} / {self.garage.max_failed}",
            font=("VT323", 14),
            fill="red",
            tags="stats"
        )