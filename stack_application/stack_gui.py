import tkinter as tk
from tkinter import ttk, messagebox
from .stack_logic import ParkingManager

class StackPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.logic = ParkingManager()
        self.car_visuals = {} # Stores the "ID" of cars on the canvas

        # 1. THE CANVAS (This draws your Canva background)
        self.canvas = tk.Canvas(self, width=1024, height=576)
        self.canvas.pack(fill="both", expand=True)
        
        # Load your Canva background
        self.bg_img = tk.PhotoImage(file="stack_bg.png")
        self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
        
        # Load your car icon (ensure this filename matches your photo!)
        self.car_img = tk.PhotoImage(file="cars.png")

        # 2. THE TABLE (The "Treeview")
        # Matches your middle box: No., Plate Number, Arrival, Departure
        self.tree = ttk.Treeview(self, columns=("No", "Plate", "In", "Out"), show='headings')
        self.tree.heading("No", text="Slot")
        self.tree.heading("Plate", text="Plate Number")
        self.tree.heading("In", text="Arrival")
        self.tree.heading("Out", text="Departure")
        
        # Placing it in the middle purple area
        self.tree.place(x=250, y=110, width=320, height=400)

        # 3. INPUTS (Right side purple box)
        self.plate_label = tk.Label(self, text="ENTER PLATE:", bg="#b19cd9") # Matches purple theme
        self.plate_label.place(x=620, y=170)
        
        self.plate_entry = tk.Entry(self, font=("Arial", 12))
        self.plate_entry.place(x=620, y=200, width=150)
        
        park_btn = tk.Button(self, text="PARK", command=self.handle_park, bg="green", fg="white")
        park_btn.place(x=620, y=240, width=70)
        
        exit_btn = tk.Button(self, text="EXIT", command=self.handle_exit, bg="red", fg="white")
        exit_btn.place(x=700, y=240, width=70)

    # Where the cars appear on the left (Slots 1-10)
    def get_slot_coords(self, slot_num):
        # Slot 1 is at the bottom, Slot 10 is at the top
        bottom_y = 480 
        gap = 42 
        return (100, bottom_y - ((slot_num - 1) * gap))

    def handle_park(self):
        plate = self.plate_entry.get().upper()
        if not plate:
            messagebox.showwarning("Warning", "Plate Number required!")
            return

        car, error = self.logic.park_car(plate)
        if car:
            # Update Table
            self.tree.insert("", "end", iid=car.plate_number, values=(car.slot, car.plate_number, car.arrival, car.departure))
            
            # Show Car visually in the "Entrance/Exit" area
            x, y = self.get_slot_coords(len(self.logic.stack))
            car_id = self.canvas.create_image(x, y, image=self.car_img)
            self.car_visuals[car.plate_number] = car_id
            
            self.plate_entry.delete(0, tk.END)
        else:
            messagebox.showerror("Error", error)

    def handle_exit(self):
        car = self.logic.exit_car()
        if car:
            # Update Departure in Table
            self.tree.item(car.plate_number, values=(car.slot, car.plate_number, car.arrival, car.departure))
            
            # Remove car from visual (LIFO - Last In First Out)
            car_id = self.car_visuals.get(car.plate_number)
            if car_id:
                self.canvas.delete(car_id)
            
            messagebox.showinfo("Success", f"Car {car.plate_number} exited from {car.slot}")
        else:
            messagebox.showwarning("Empty", "Garage is already empty!")