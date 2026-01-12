from tkinter import *
import tkinter as tk
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk
import tkinter.font as tkfont
import os

class TowerOfHanoiGUI(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        # -----------------------------
        # Window settings
        # -----------------------------

        self.title = "Tower of Hanoi"
        self.delay = 500
        self.max_disks = 7

        self.canvas_width = 1531
        self.canvas_height = 789
        
        self.disk_height = 40
        self.disk_width_increment = 34
        self.base_height = 80
        self.base_color = "#6b4fd6"
        self.stack_width = 15
        self.stack_height = 340

        self.colors = ["#ef476f", "#f78c6b", "#ffd166",
                       "#06d6a0", "#118ab2", "#073b4c"]

        if isinstance(parent, (tk.Tk, tk.Toplevel)):
            parent.title(self.title)
            parent.geometry(f"{self.canvas_width}x{self.canvas_height}")
            parent.resizable(True, True)
            self.root = parent

        # -----------------------------
        # Fonts
        # -----------------------------
        self.ui_font = tkfont.Font(family="VT323", size=20)

        # -----------------------------
        # Canvas
        # -----------------------------
        self.canvas = Canvas(
            parent,
            width=self.canvas_width,
            height=self.canvas_height,
            highlightthickness=0
        )
        self.canvas.pack()

        # -----------------------------
        # Background image
        # -----------------------------
        base_dir = os.path.dirname(os.path.abspath(__file__))
        bg_path = os.path.join(base_dir, "hanoi_bg.png")
        try:
            bg_image = Image.open(bg_path).resize(
                (self.canvas_width, self.canvas_height),
                Image.NEAREST
            )
            self.bg_img = ImageTk.PhotoImage(bg_image)
        except FileNotFoundError:
            self.bg_img = None

        # -----------------------------
        # Controls Frame (full width, colored background)
        # -----------------------------
        controls_height = 50
        controls_frame = Frame(parent, width=1490, height=controls_height, bg="#3b2f9a")
        controls_frame.place(x=22, y=60)  # below title area
        controls_frame.pack_propagate(False)  # fix height

        # Inner frame for centering contents
        inner_frame = Frame(controls_frame, bg="#3b2f9a")
        inner_frame.pack(expand=True)

        # Label + Entry
        Label(inner_frame, text="DISKS (5–7):", font=self.ui_font, bg="#3b2f9a", fg="white").pack(side=LEFT, padx=5)
        self.enter_disks = Entry(inner_frame, font=self.ui_font,
                                 width=5, justify="center")
        self.enter_disks.insert(0, str(self.max_disks))
        self.enter_disks.pack(side=LEFT, padx=5)

        # Buttons (slightly smaller than control bar)
        buttons = [
            ("START", self.auto),
            ("STOP", self.stop),
            ("PREV", self.previous_step),
            ("NEXT", self.next_step),
            ("RESET", self.generate)
        ]

        for text, cmd in buttons:
            Button(
                inner_frame,
                text=text,
                font=self.ui_font,
                bg="#9b8cff",
                fg="white",
                relief="flat",
                padx=5,   
                pady=3,    
                command=cmd
            ).pack(side=LEFT, padx=5)

        # -----------------------------
        # Hanoi state
        # -----------------------------
        self.state = 0
        self.num_disks = self.max_disks
        self.states = []
        self.auto_running = False

        self.generate()

    # -----------------------------
    # Hanoi logic
    # -----------------------------
    def move(self, number, stack_from, stack_to):
        if number == 1:
            self.stacks[stack_to].append(self.stacks[stack_from].pop())
            self.states.append([[j for j in self.stacks[i]] for i in range(3)])
        else:
            aux = 3 - stack_from - stack_to
            self.move(number - 1, stack_from, aux)
            self.move(1, stack_from, stack_to)
            self.move(number - 1, aux, stack_to)

    def hanoi(self, size):
        self.stacks = [[] for _ in range(3)]
        self.stacks[0] = [size - i for i in range(size)]
        self.states = [[[j for j in self.stacks[i]] for i in range(3)]]
        self.move(size, 0, 2)
        return self.states

    def generate(self):
        try:
            entered = int(self.enter_disks.get())
            if entered < 5 or entered > 7:
                raise ValueError
            self.num_disks = entered
        except ValueError:
            messagebox.showerror(
                "Invalid Input",
                "Please enter a number between 5 and 7."
            )
            self.enter_disks.delete(0, END)
            self.enter_disks.insert(0, str(self.max_disks))
            return

        self.state = 0
        self.states = self.hanoi(self.num_disks)
        self.draw_current_state()

    def next_step(self):
        self.state = (self.state + 1) % len(self.states)
        self.draw_current_state()

    def previous_step(self):
        self.state = (self.state - 1) % len(self.states)
        self.draw_current_state()

    # -----------------------------
    # Drawing
    # -----------------------------
    def get_stack_x(self, i):
        return (self.canvas_width // 3) * i + (self.canvas_width // 6)

    def draw_base(self):
        y = self.canvas_height - self.base_height
        self.canvas.create_rectangle(
            0, y, self.canvas_width, self.canvas_height,
            fill=self.base_color, outline=""
        )

        for i in range(3):
            x = self.get_stack_x(i)
            self.canvas.create_rectangle(
                x, y - self.stack_height,
                x + self.stack_width, y,
                fill=self.base_color, outline=""
            )

    def draw_stack(self, i, stacks):
        center = self.get_stack_x(i) + self.stack_width // 2
        y = self.canvas_height - self.base_height - \
            self.disk_height * len(stacks[i])

        for disk in reversed(stacks[i]):
            width = disk * self.disk_width_increment + 30
            self.canvas.create_rectangle(
                center - width // 2, y,
                center + width // 2, y + self.disk_height,
                fill=self.colors[(disk - 1) % len(self.colors)],
                outline=""
            )
            y += self.disk_height

    def draw_current_state(self):
        self.canvas.delete("all")
        if self.bg_img:
            self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")

        self.draw_base()
        state = self.states[self.state]

        for i in range(3):
            self.draw_stack(i, state)

        self.canvas.create_text(
            self.canvas_width // 2,
            self.canvas_height - 40,
            text=f"MOVES: {self.state}",
            font=self.ui_font,
            fill="white"
        )

    # -----------------------------
    # Auto solve
    # -----------------------------
    def auto_step(self):
        if not self.auto_running or self.state == len(self.states) - 1:
            self.auto_running = False
            return

        self.next_step()
        self.after(self.delay, self.auto_step)

    def auto(self):
        self.auto_running = True
        self.after(self.delay, self.auto_step)

    def stop(self):
        self.auto_running = False


# -----------------------------
# Run program
# -----------------------------
if __name__ == "__main__":
    root = Tk()
    TowerOfHanoiGUI(root)
    root.mainloop()