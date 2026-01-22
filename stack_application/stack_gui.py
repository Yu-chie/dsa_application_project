import tkinter as tk
from tkinter import ttk, messagebox

class StackGui(tk.Frame):
    def __init__(self, parent, garage_logic, controller):
        super().__init__(parent, bg="#330084")
        self.garage = garage_logic
        self.controller = controller

        # Title
        title_label = tk.Label(
            self, text="STACK PARKING GARAGE", 
            font=("VT323", 30), bg="#330084", fg="#ecb1ff"
        )
        title_label.pack(pady=20)

        # Main Container
        main_container = tk.Frame(self, bg="#330084")
        main_container.pack(fill="both", expand=True, padx=50)

        # --- LEFT SIDE: INPUT & CONTROLS ---
        control_frame = tk.Frame(main_container, bg="#330084")
        control_frame.pack(side="left", fill="y", padx=20)

        tk.Label(control_frame, text="Plate Number:", font=("VT323", 16), bg="#330084", fg="white").pack(anchor="w")
        self.plate_entry = tk.Entry(control_frame, font=("Arial", 14))
        self.plate_entry.pack(fill="x", pady=5)

        btn_style = {"font": ("VT323", 14), "bg": "#ecb1ff", "fg": "#330084", "activebackground": "#ffffff", "pady": 5}

        tk.Button(control_frame, text="PARK CAR", command=self.park_car, **btn_style).pack(fill="x", pady=10)
        tk.Button(control_frame, text="REMOVE TOP (POP)", command=self.pop_car, **btn_style).pack(fill="x", pady=5)
        tk.Button(control_frame, text="REMOVE SPECIFIC", command=self.remove_specific, **btn_style).pack(fill="x", pady=5)

        # --- MIDDLE: VISUAL STACK ---
        stack_frame = tk.Frame(main_container, bg="#330084")
        stack_frame.pack(side="left", fill="both", expand=True, padx=20)
        
        tk.Label(stack_frame, text="GARAGE STACK (Top at Bottom)", font=("VT323", 16), bg="#330084", fg="white").pack()
        self.stack_listbox = tk.Listbox(stack_frame, font=("VT323", 18), bg="#594faf", fg="white", justify="center")
        self.stack_listbox.pack(fill="both", expand=True)

        # --- RIGHT SIDE: TRANSACTION TABLE ---
        table_frame = tk.Frame(main_container, bg="#330084")
        table_frame.pack(side="right", fill="both", expand=True)

        tk.Label(table_frame, text="HISTORY LOG", font=("VT323", 16), bg="#330084", fg="white").pack()
        
        self.tree = ttk.Treeview(table_frame, columns=("Plate", "Arr", "Dep"), show="headings", height=10)
        self.tree.heading("Plate", text="Plate Number")
        self.tree.heading("Arr", text="Arrivals")
        self.tree.heading("Dep", text="Departures")
        self.tree.column("Plate", width=100)
        self.tree.column("Arr", width=50)
        self.tree.column("Dep", width=50)
        self.tree.pack(fill="both", expand=True)

        self.update_display()

    def park_car(self):
        plate = self.plate_entry.get().upper()
        if not plate:
            messagebox.showwarning("Input Error", "Please enter a plate number.")
            return
        
        success, msg = self.garage.park_car(plate)
        if success:
            self.plate_entry.delete(0, tk.END)
            self.update_display()
        else:
            messagebox.showerror("Error", msg)

    def pop_car(self):
        success, msg = self.garage.remove_top_car()
        if success:
            self.update_display()
        else:
            messagebox.showerror("Error", msg)

    def remove_specific(self):
        plate = self.plate_entry.get().upper()
        if not plate:
            messagebox.showwarning("Input Error", "Enter plate to remove.")
            return
        
        success, msg = self.garage.remove_specific_car(plate)
        if success:
            self.plate_entry.delete(0, tk.END)
            self.update_display()
            messagebox.showinfo("Shuffle Pop", msg)
        else:
            messagebox.showerror("Error", msg)

    def update_display(self):
        # Update Visual Stack
        self.stack_listbox.delete(0, tk.END)
        # Displaying so top of stack is at the bottom visually (like a garage floor)
        for car in reversed(self.garage.garage_stack):
            self.stack_listbox.insert(tk.END, f"|  {car.plate_number}  |")
        
        # Update Table
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # We show all cars currently in garage for the table
        for car in self.garage.garage_stack:
            self.tree.insert("", tk.END, values=(car.plate_number, car.arrival_count, car.departure_count))
