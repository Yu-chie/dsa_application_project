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
            "queue_application/queue_gui/queue_bg3.png"
        ]
        self.bg_image = None
        for p in bg_path_candidates:
            try:
                self.bg_image = Image.open(p)
                break
            except FileNotFoundError:
                continue
        if self.bg_image is None:
            raise FileNotFoundError("Background image not found. Place queue_bg_custom.png or queue_bg3.png in queue_application/queue_gui/")
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
        plate = simpledialog.askstring("Car Arrives", "Enter the car's plate number:")
        if not plate:
            return
        self.car_arrives(plate)
        
    def auto_arrival(self):
        if not self.running or not self.auto_arrival_running:
            return

        plate = f"CAR-{random.randint(100,999)}"
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
        """
        Simplified overlay: the background image already contains the table grid.
        This method only draws the table data (slot / plate / arrivals / departures)
        aligned over the background (no headers/grid lines).
        """
        self.canvas.delete("table")

        # Adjust coordinates to match the background layout
        start_x = 160     # leftmost column (slot number)
        col_gap = 180     # horizontal gap between columns
        start_y = 140     # top of first row
        row_gap = 80      # vertical spacing between rows

        for i, car in enumerate(self.garage.queue):
            y = start_y + i * row_gap
            slot_text = i + 1
            plate_text = "-" if car is None else car['plate_number']
            arrivals_text = "-" if car is None else str(car['arrival_count'])
            departures_text = "-" if car is None else str(car['departure_count'])

            values = [slot_text, plate_text, arrivals_text, departures_text]
            for j, value in enumerate(values):
                self.canvas.create_text(
                    start_x + j * col_gap, y,
                    text=value,
                    font=("VT323", 14),
                    tags="table"
                )
        
    def resize_bg(self, event):
        # Resize background
        resized_bg = self.bg_image.resize((event.width, event.height))
        self.bg_photo = ImageTk.PhotoImage(resized_bg)
        self.canvas.itemconfig(self.bg_image_id, image=self.bg_photo)
        
        # Reposition control buttons to upper-right
        right_x = event.width - 40
        self.canvas.coords(self.mode_label_window, right_x, PANEL_Y_MODE - 40)
        self.canvas.coords(self.manual_btn_window, right_x, PANEL_Y_MODE)
        self.canvas.coords(self.auto_btn_window, right_x, PANEL_Y_MODE + 40)

        self.canvas.coords(self.queue_label_window, right_x, PANEL_Y_QUEUE - 40)
        self.canvas.coords(self.arrive_btn_window, right_x, PANEL_Y_QUEUE)
        self.canvas.coords(self.depart_btn_window, right_x, PANEL_Y_QUEUE + 40)

        self.draw_waiting_area()

    def draw_waiting_area(self):
        self.canvas.delete("waiting")
        
        for i, car in enumerate(self.garage.waiting):
            x = WAITING_X_START + i * WAITING_GAP

            self.canvas.create_text(
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