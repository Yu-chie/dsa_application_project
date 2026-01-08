import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
from queue_application.parking_garage import ParkingGarage
import random 

# Control Panel Layout (Upper Right Box)
CONTROL_X = 1400
CONTROL_Y = 250

WAITING_X_START = 1150
WAITING_Y_IMAGE = 600
WAITING_Y_TEXT = 690
WAITING_GAP = 220

class QueueGUI(tk.Frame):
    def __init__(self, parent, garage, controller):
        super().__init__(parent)
        self.garage = garage
        self.controller = controller
        self.running = True
        
        self.auto_arrival_running = False
        self.auto_depart_running = False
        
        # Canvas setup
        self.canvas = tk.Canvas(self)
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self.resize_bg)
        
        # Background image: prefer user-supplied custom background, fallback to existing
        bg_path_candidates = [
            "queue_application/queue_gui/queue_bg_custom.png",
            "queue_application/queue_gui/queue_bg4.png"
        ]
        self.bg_image = None
        for p in bg_path_candidates:
            try:
                self.bg_image = Image.open(p)
                break
            except FileNotFoundError:
                continue
        if self.bg_image is None:
            raise FileNotFoundError("Background image not found. Place queue_bg_custom.png or queue_bg4.png in queue_application/queue_gui/")
        self.bg_photo = ImageTk.PhotoImage(self.bg_image.resize((1920, 1080)))
        self.bg_image_id = self.canvas.create_image(0, 0, image=self.bg_photo, anchor="nw")
        
        # Buttons inside upper right box
        self.manual_btn = tk.Button(
            self,
            text="MANUAL",
            font=("VT323", 14),
            width=15,
            command=lambda: self.set_mode("MANUAL")
        )

        self.manual_btn_window = self.canvas.create_window(
            CONTROL_X - 80, CONTROL_Y,
            window=self.manual_btn
        )

        self.auto_btn = tk.Button(
            self,
            text="AUTO",
            font=("VT323", 14),
            width=15,
            command=lambda: self.set_mode("AUTO")
        )

        self.auto_btn_window = self.canvas.create_window(
            CONTROL_X + 80, CONTROL_Y,
            window=self.auto_btn
        )

        self.arrive_btn = tk.Button(
            self,
            text="CAR ARRIVES",
            font=("VT323", 14),
            width=15,
            command=self.handle_arrive_click
        )
        
        self.arrive_btn_window = self.canvas.create_window(
            CONTROL_X - 80, CONTROL_Y + 60,
            window=self.arrive_btn
        )

        self.depart_btn = tk.Button(
            self,
            text="CAR DEPARTS",
            font=("VT323", 14),
            width=15,
            command=self.handle_depart_click
        )
        
        self.depart_btn_window = self.canvas.create_window(
            CONTROL_X + 80, CONTROL_Y + 60,
            window=self.depart_btn
        )
        
        if self.garage.mode == "AUTO":
            self.arrive_btn.config(state="disabled")
            self.depart_btn.config(state="disabled")
        
        # Game loop
        if self.garage.mode == "AUTO":
            self.auto_arrival_running = True
            self.auto_depart_running = True
            self.auto_arrival()
            self.auto_depart()
        elif self.garage.mode == "MANUAL":
            pass  # slower arrivals
        
        # cars
        self.car_images = []
        self.load_car_images()
        
        self.draw_table()
        self.draw_stats()
        self.draw_waiting_area()
        self.tick()                
        
    def load_car_images(self):
        self.car_images.clear()

        for i in range(1, 11):
            path = f"queue_application/queue_gui/cars/C{str(i).zfill(2)}.PNG"
            img = Image.open(path).resize((90, 150))
            self.car_images.append(ImageTk.PhotoImage(img))
        
    def car_arrives(self, plate=None):
        if self.garage.game_over:
            return
        # If plate provided, park that car immediately (manual arrival).
        if plate:
            result = self.garage.car_arrives(plate)
            messagebox.showinfo("Car Arrives", result)
            self.draw_table()
            self.draw_stats()
            return
        
        # Otherwise, process next waiting car (auto arrival)
        if not self.garage.waiting:
            messagebox.showinfo("Info", "No cars waiting")
            return
        
        car = self.garage.waiting.pop(0)
        result = self.garage.car_arrives(car["plate_number"])
        messagebox.showinfo("Car Arrives", result)
        self.draw_table()
        self.draw_waiting_area()
        self.draw_stats()

    def handle_arrive_click(self):
        if self.garage.mode != "MANUAL":
            messagebox.showwarning(
                "Invalid Action",
                "Please switch to MANUAL mode to control the queue."
            )
            return
        plate = self.garage.get_random_plate()
        if not plate:
            messagebox.showinfo("No Cars", "No available cars to add.")
            return
        self.car_arrives(plate)
        
    def auto_arrival(self):
        if not self.running or not self.auto_arrival_running:
            return

        # if there is space, move waiting car to parking in auto mode
        if self.garage.waiting and None in self.garage.queue:
            car = self.garage.waiting.pop(0)
            self.garage.car_arrives(car["plate_number"])
            self.draw_table()
        
        # Add new car to waiting area
        plate = self.garage.get_random_plate()
        if plate:
            self.garage.add_to_waiting(plate)

        self.draw_waiting_area()
        self.draw_stats()

        self.after(3000, self.auto_arrival)

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

    def handle_depart_click(self):
        if self.garage.mode != "MANUAL":
            messagebox.showwarning(
                "Invalid Action",
                "Please switch to MANUAL mode to control the queue."
            )
            return
        self.car_departs()
    
    def auto_depart(self):
        if not self.running or not self.auto_depart_running:
            return

        for car in self.garage.queue:
            if car:
                self.garage.car_departs(car['plate_number'])
                break

        self.draw_table()
        self.draw_stats()
        self.after(5000, self.auto_depart)
    
    def set_mode(self, mode):
        if self.garage.mode == mode:
            return

        self.garage.mode = mode

        if mode == "AUTO":
            self.arrive_btn.config(state="disabled")
            self.depart_btn.config(state="disabled")

            if not self.auto_arrival_running:
                self.auto_arrival_running = True
                self.auto_arrival()

            if not self.auto_depart_running:
                self.auto_depart_running = True
                self.auto_depart()

        else:  # MANUAL
            self.arrive_btn.config(state="normal")
            self.depart_btn.config(state="normal")

            self.auto_arrival_running = False
            self.auto_depart_running = False

    def draw_table(self):
        self.canvas.delete("table")

        # Adjust coordinates to match the background layout
        start_x = 100     # leftmost column (slot number)
        col_gap = 160     # horizontal gap between columns
        start_y = 120     # top of first row
        row_gap = 65      # vertical spacing between rows

        for i, car in enumerate(self.garage.queue):
            y = start_y + i * row_gap
            
            # column 0 - slot number
            self.canvas.create_text(
                start_x,
                y,
                text=str(i + 1),
                font=("VT323", 14),
                tags="table"
            )
            
            # column 1 - car image
            if car is not None:
                self.canvas.create_image(
                    start_x + col_gap,
                    y,
                    image=self.car_images[i % len(self.car_images)],
                    tags="table"
                )
            else:
                self.canvas.create_text(
                    start_x + col_gap,
                    y,
                    text="-",
                    font=("VT323", 14),
                    tags="table"
                )
                
            # column 2 — plate number
            self.canvas.create_text(
                start_x + col_gap * 2,
                y,
                text="-" if car is None else car["plate_number"],
                font=("VT323", 14),
                tags="table"
            )

            # column 3 — arrivals
            self.canvas.create_text(
                start_x + col_gap * 3,
                y,
                text="-" if car is None else car["arrival_count"],
                font=("VT323", 14),
                tags="table"
            )

            # column 4 — departures
            self.canvas.create_text(
                start_x + col_gap * 4,
                y,
                text="-" if car is None else car["departure_count"],
                font=("VT323", 14),
                tags="table"
            )
        
    def resize_bg(self, event):
        # Resize background
        resized_bg = self.bg_image.resize((event.width, event.height))
        self.bg_photo = ImageTk.PhotoImage(resized_bg)
        self.canvas.itemconfig(self.bg_image_id, image=self.bg_photo)
        
        self.draw_waiting_area()

    def draw_waiting_area(self):
        self.canvas.delete("waiting")
        
        for i, car in enumerate(self.garage.waiting):
            x = WAITING_X_START + i * WAITING_GAP

            # car image
            self.canvas.create_image(
                x,
                WAITING_Y_IMAGE,
                image=self.car_images[i % len(self.car_images)],
                tags="waiting"
            )

            # waiting time
            color = "red" if car['time_left'] <= 2 else "white"
            
            self.canvas.create_text(
                x,
                WAITING_Y_TEXT,
                text=f"Time Left: {car['time_left']}s",
                font=("VT323", 12),
                fill=color,
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
        self.draw_stats()
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