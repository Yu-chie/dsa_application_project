from operator import index
import tkinter as tk
from tkinter import simpledialog, messagebox
from PIL import Image, ImageTk
from queue_application.parking_garage import ParkingGarage
import random 

# Control Panel Layout (Upper Right Box)
CONTROL_X = 1200
CONTROL_Y = 225

WAITING_X_START = 990
WAITING_Y_IMAGE = 590
WAITING_Y_TEXT = 650
WAITING_GAP = 200

class QueueGUI(tk.Frame):
    def __init__(self, parent, garage, controller):
        super().__init__(parent)
        self.garage = garage
        self.controller = controller
        self.running = True
        self.is_active = False
        
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
        
        # Manual & AUto button
        self.manual_btn = tk.Button(
            self,
            text="MANUAL",
            font=("VT323", 14),
            width=15,
            command=lambda: self.set_mode("MANUAL")
        )

        self.manual_btn_window = self.canvas.create_window(
            CONTROL_X - 90, CONTROL_Y,
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
            CONTROL_X + 90, CONTROL_Y,
            window=self.auto_btn
        )
        
        # Arrive & Depart buttons
        self.arrive_btn = tk.Button(
            self,
            text="CAR ARRIVES",
            font=("VT323", 14),
            width=15,
            command=self.handle_arrive_click
        )
        
        self.arrive_btn_window = self.canvas.create_window(
            CONTROL_X - 90, CONTROL_Y + 60,
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
            CONTROL_X + 90, CONTROL_Y + 60,
            window=self.depart_btn
        )

        # Retry button (top-right)
        self.retry_btn = tk.Button(
            self,
            text="RETRY",
            font=("VT323", 14),
            width=15,
            command=self.retry_game
        )

        self.retry_btn_window = self.canvas.create_window(
            CONTROL_X - 90, 170,
            window=self.retry_btn
        )
        
        # New game button (below retry)
        self.new_game_btn = tk.Button(
            self,
            text="NEW GAME",
            font=("VT323", 14),
            width=15,
            command=self.new_game
        )

        self.new_game_btn_window = self.canvas.create_window(
            CONTROL_X + 90, 170,
            window=self.new_game_btn
        )
        
        if self.garage.mode == "AUTO":
            self.arrive_btn.config(state="disabled")
            self.depart_btn.config(state="disabled")
        
        # Start and Stop Button
        self.start_btn = tk.Button(
            self,
            text="START",
            font=("VT323", 14),
            width=15,
            command=self.start_simulation
        )
        
        self.start_btn_window = self.canvas.create_window(
            CONTROL_X - 90, CONTROL_Y + 120,
            window=self.start_btn
        )

        self.stop_btn = tk.Button(
            self,
            text="STOP",
            font=("VT323", 14),
            width=15,
            command=self.stop_simulation
        )

        self.stop_btn_window = self.canvas.create_window(
            CONTROL_X + 90, CONTROL_Y + 120,
            window=self.stop_btn
        )

        # Status message
        self.status_text_id = None
        self.status_clear_job = None
        
        # cars
        self.selected_index = None
        self.car_images = []
        self.load_car_images()
        
        # selection state
        self.selected_waiting_index = None
        self.selected_queue_index = None
        
        # Game loop
        if self.garage.mode == "AUTO":
            self.auto_arrival_running = True
            self.auto_depart_running = True
            self.auto_depart()
            self.auto_arrival()
        elif self.garage.mode == "MANUAL":
            self.manual_arrival()

        self.draw_table()
        self.draw_stats()
        self.draw_waiting_area()                
        
    def load_car_images(self):
        self.car_images.clear()

        for i in range(1, 11):
            path = f"queue_application/queue_gui/cars/C{str(i).zfill(2)}.PNG"
            img = Image.open(path).resize((90, 90))
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
        
        if self.selected_waiting_index is None:
            self.set_status("Select a waiting car first", "yellow")
            return
        
        car = self.garage.waiting.pop(self.selected_waiting_index)
        result = self.garage.car_arrives(car["plate_number"])
        messagebox.showinfo("Car Arrives", result)
        self.draw_table()
        self.draw_waiting_area()
        self.draw_stats()

    def handle_arrive_click(self):
        if self.garage.mode != "MANUAL":
            self.set_status("Switch to MANUAL mode", "red")
            return

        if not self.garage.waiting:
            self.set_status("No cars waiting", "yellow")
            return

        # FIFO arrival → always take the FRONT car
        car = self.garage.waiting.pop(0)
        result = self.garage.car_arrives(car["plate_number"])

        self.selected_waiting_index = None
        self.set_status(result, color="lightgreen")
        self.draw_table()
        self.draw_waiting_area()
        self.draw_stats()

    def auto_arrival(self):
        if not self.running or not self.is_active or not self.auto_arrival_running:
            return

        if self.garage.mode == "AUTO":
            if self.garage.waiting and None in self.garage.queue:
                car = self.garage.waiting.pop(0)
                self.garage.car_arrives(car["plate_number"])

            plate = self.garage.get_random_plate()
            if plate:
                self.garage.add_to_waiting(plate)

        self.draw_waiting_area()
        self.draw_table()
        self.draw_stats()

        self.after(3000, self.auto_arrival)

    def manual_arrival(self):
        if not self.running or self.garage.mode != "MANUAL":
            return

        plate = self.garage.get_random_plate()
        if plate:
            self.garage.add_to_waiting(plate)
            self.draw_waiting_area()
            self.draw_stats()

        self.after(4000, self.manual_arrival)  # slower than auto

    def car_departs(self):
        if self.garage.game_over:
            return
        
        plate = simpledialog.askstring("Car Departs", "Enter the car's plate number:")
        if not plate:
            return
        result = self.garage.car_departs(plate)
        self.set_status(result, color="orange")
        self.draw_table()
        self.draw_stats()

    def handle_depart_click(self):
        if self.garage.mode != "MANUAL":
            return

        if self.selected_queue_index is None:
            messagebox.showerror("Error", "No car selected in the queue.")
            return

        # Get the selected car's plate number
        plate = self.garage.queue[self.selected_queue_index]["plate_number"]

        if self.selected_queue_index == 0:
            # Depart the first car and shift others forward
            result = self.garage.car_departs(plate)
        else:
            # Depart cars in front, re-enter them at the end, then depart the selected car
            temp_queue = []
            for i in range(self.selected_queue_index):
                car = self.garage.queue[i]
                if car is not None:
                    temp_queue.append(car["plate_number"])

            # Depart the selected car
            result = self.garage.car_departs(plate)

            # Re-enter cars in front at the end of the queue
            for plate_number in temp_queue:
                self.garage.car_arrives(plate_number)

        self.selected_queue_index = None
        self.set_status(result, "orange")
        self.draw_table()
        self.draw_stats()
        
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
            if car:
                img_id = self.canvas.create_image(
                    start_x + col_gap,
                    y,
                    image=self.get_car_image(car["plate_number"]),
                    tags=("table", "queue_car", f"queue_{i}")
                )

                self.canvas.tag_bind(
                    f"queue_{i}",
                    "<Button-1>",
                    lambda e, idx=i: self.select_queue_car(idx)
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
        
        if i == self.selected_queue_index:
            self.canvas.create_rectangle(
                start_x + col_gap - 50,
                y - 40,
                start_x + col_gap + 50,
                y + 40,
                outline="orange",
                width=3,
                tags="table"
            )
        
        self.canvas.tag_bind(
            "queue_car",
            "<Button-1>",
            self.on_queue_click
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
                image=self.get_car_image(car['plate_number']),
                tags=("waiting", f"waiting_{i}")
            )
            
            # car plate
            self.canvas.create_text(
                x,
                WAITING_Y_IMAGE - 40,
                text=car['plate_number'],
                font=("VT323", 12),
                tags=("waiting", f"waiting_{i}")
            )
            
            # waiting time
            color = "red" if car['time_left'] <= 2 else "white"
            self.canvas.create_text(
                x,
                WAITING_Y_TEXT,
                text=f"{car['time_left']}s",
                font=("VT323", 12),
                fill=color,
                tags=("waiting", f"waiting_{i}")
            )
            
            # highlight selected car
            if i == self.selected_waiting_index:
                self.canvas.create_rectangle(
                    x-50, WAITING_Y_IMAGE-50,
                    x+50, WAITING_Y_IMAGE+50,
                    outline="cyan",
                    width=3,
                    tags="waiting"
                )
            
            self.canvas.tag_bind(
                f"waiting_{i}",
                "<Button-1>",
                lambda e, idx=i: self.select_waiting_car(idx)
            )

    def stop(self):
        self.running = False
        self.destroy()
        
    def start_simulation(self):
        if not self.is_active:
            self.is_active = True
            self.set_status("SIMULATION STARTED", "lightgreen")
            self.tick() # Start the main game loop
            if self.garage.mode == "AUTO":
                self.auto_arrival()
                self.auto_depart()
            else:
                self.manual_arrival()

    def stop_simulation(self):
        self.running = False
        self.is_active = False
        self.set_status("SIMULATION PAUSED", "red")
        self.auto_arrival_running = False
        self.auto_depart_running = False
        # Ensure no new cars enter the waiting area
        self.after_cancel(self.manual_arrival)  # Cancel manual arrival loop
        self.after_cancel(self.auto_arrival)    # Cancel auto arrival loop

        
    def tick(self):
        if not self.running or not self.is_active:
            return
        
        if self.garage.game_over:
            messagebox.showerror(
                "GAME OVER",
                f"Too many cars failed!\nFinal Score: {self.garage.score}"
            )
            self.arrive_btn.config(state="disabled")
            self.depart_btn.config(state="disabled")   
            if messagebox.askyesno("Game Over", "Retry the game?"):
                self.retry_game()
                self.arrive_btn.config(state="normal")
                self.depart_btn.config(state="normal")   
            else:
                self.stop()

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
    
    def get_car_image(self, plate):
        index = int(plate[3:]) - 1      # COI is 0
        return self.car_images[index]

    def retry_game(self):
        self.auto_arrival_running = False
        self.auto_depart_running = False
        self.garage.reset_game_state()
        self.draw_table()
        self.draw_waiting_area()
        self.draw_stats()
        self.auto_arrival_running = (self.garage.mode == "AUTO")
        self.auto_depart_running = (self.garage.mode == "AUTO")

        if self.garage.mode == "AUTO":
            self.auto_arrival()
            self.auto_depart()

    def new_game(self):
        self.auto_arrival_running = False
        self.auto_depart_running = False
        if messagebox.askyesno("Confirm", "This will erase all records. Continue?"):
            self.garage.reset_all()
            self.draw_table()
            self.draw_waiting_area()
            self.draw_stats()
            self.auto_arrival_running = (self.garage.mode == "AUTO")
            self.auto_depart_running = (self.garage.mode == "AUTO")

            if self.garage.mode == "AUTO":
                self.auto_arrival()
                self.auto_depart()

    def set_status(self, message, color="white", duration=2000):
        # Remove old status
        if self.status_text_id:
            self.canvas.delete(self.status_text_id)

        # Cancel pending clear
        if self.status_clear_job:
            self.after_cancel(self.status_clear_job)

        # Draw new status message
        self.status_text_id = self.canvas.create_text(
            960, 820,                     # adjust position if needed
            text=message,
            font=("VT323", 18, "bold"),
            fill=color,
            tags="status"
        )

        # Auto-clear message
        self.status_clear_job = self.after(duration, self.clear_status)

    def clear_status(self):
        if self.status_text_id:
            self.canvas.delete(self.status_text_id)
            self.status_text_id = None

    def select_waiting_car(self, index):
        self.selected_waiting_index = index
        self.selected_queue_index = None
        self.set_status(
            f"Selected {self.garage.waiting[index]['plate_number']} for arrival",
            color="lightblue"
        )

    def select_queue_car(self, index):
        car = self.garage.queue[index]
        if not car:
            return

        self.selected_queue_index = index
        self.selected_waiting_index = None
        self.set_status(
            f"Selected {car['plate_number']} for departure",
            color="orange"
        )
    
    def on_queue_click(self, event):
        item = self.canvas.find_withtag("current")
        tags = self.canvas.gettags(item)
        for tag in tags:
            if tag.startswith("queue_"):
                index = int(tag.split("_")[1])
                self.select_queue_car(index)
                break

    def update_simulation(self):
        if self.garage.mode == "AUTO":
            # In AUTO mode, everything is automatic
            self.garage.update_waiting()
            self.garage.update_parking()
        elif self.garage.mode == "MANUAL":
            # In MANUAL mode, only the waiting area is automatic
            self.garage.update_waiting()

        self.draw_table()
        self.draw_stats()
