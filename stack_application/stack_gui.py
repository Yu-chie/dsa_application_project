import tkinter as tk
from tkinter import ttk, messagebox
from stack_logic import ParkingManager

class StackPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.logic = ParkingManager()
        self.car_visuals = {}

        self.canvas = tk.Canvas(self, width=1024, height=576)
        self.canvas.pack(fill="both", expand=True)
        
        # Fixed paths for your folder structure
        self.bg_img = tk.PhotoImage(file="stack_bg.png")
        self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
        self.car_img = tk.PhotoImage(file="cars.png")

        self.tree = ttk.Treeview(self, columns=("No", "Plate", "In", "Out"), show='headings')
        self.tree.heading("No", text="Slot")
        self.tree.heading("Plate", text="Plate Number")
        self.tree.heading("In", text="Arrival")
        self.tree.heading("Out", text="Departure")
        self.tree.place(x=250, y=110, width=320, height=400)

        self.plate_entry = tk.Entry(self, font=("Arial", 12))
        self.plate_entry.place(x=620, y=200, width=150)
        
        tk.Button(self, text="PARK", command=self.handle_park, bg="green", fg="white").place(x=620, y=240, width=70)
        tk.Button(self, text="EXIT", command=self.handle_exit, bg="red", fg="white").place(x=700, y=240, width=70)

    def handle_park(self):
        plate = self.plate_entry.get().upper()
        if plate:
            car, error = self.logic.park_car(plate)
            if car:
                self.tree.insert("", "end", iid=car.plate_number, values=(car.slot, car.plate_number, car.arrival, car.departure))
                self.plate_entry.delete(0, tk.END)
            else: messagebox.showerror("Error", error)

    def handle_exit(self):
        car = self.logic.exit_car()
        if car:
            self.tree.item(car.plate_number, values=(car.slot, car.plate_number, car.arrival, car.departure))
            messagebox.showinfo("Success", f"Car {car.plate_number} exited!")
        else: messagebox.showwarning("Empty", "Garage is empty!")