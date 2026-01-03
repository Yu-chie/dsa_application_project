from tkinter import *
import tkinter.messagebox as messagebox
from PIL import Image, ImageTk
import tkinter.font as tkfont
import os

class TowerOfHanoiGUI:
    def __init__(self, master):
        # -----------------------------
        # Window settings
        # -----------------------------
        self.title = "Tower of Hanoi"
        self.delay = 500
        self.max_disks = 7

        self.canvas_width = 1280
        self.canvas_height = 720

        self.disk_height = 20
        self.disk_width_increment = 16
        self.base_height = 80
        self.base_color = "#6b4fd6"
        self.stack_width = 12
        self.stack_height = 260

        self.colors = ["#ef476f", "#f78c6b", "#ffd166",
                       "#06d6a0", "#118ab2", "#073b4c"]

        master.title(self.title)
        master.geometry(f"{self.canvas_width}x{self.canvas_height}")
        master.resizable(False, False)
        self.root = master

        # -----------------------------
        # Load custom font (VT323)
        # -----------------------------
        base_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(base_dir, "VT323-Regular.ttf")

        tk_font_name = "VT323"
        self.root.tk.call('font', 'create', tk_font_name, '-family', tk_font_name, '-size', 20)
        self.ui_font = tkfont.Font(family=tk_font_name, size=22)
        self.title_font = tkfont.Font(family=tk_font_name, size=42)

        # -----------------------------
        # Canvas for Hanoi drawing
        # -----------------------------
        self.canvas = Canvas(
            master,
            width=self.canvas_width,
            height=self.canvas_height,
            highlightthickness=0
        )
        self.canvas.pack()

        # -----------------------------
        # Load background image
        # -----------------------------
        bg_path = os.path.join(base_dir, "hanoi_bg.png")
        bg_image = Image.open(bg_path).resize(
            (self.canvas_width, self.canvas_height),
            Image.NEAREST
        )
        self.bg_img = ImageTk.PhotoImage(bg_image)

        # -----------------------------
        # Frame for controls (won't be deleted)
        # -----------------------------
        self.control_frame = Frame(master, bg="#7b6cf6")
        self.control_frame.place(x=19, y=60, width=1242, height=50)

        # Entry for number of disks
        Label(self.control_frame, text="DISKS (5–7)", font=self.ui_font, bg="#7b6cf6", fg="white").pack(side=LEFT, padx=5)
        self.enter_disks = Entry(self.control_frame, font=self.ui_font, width=5, justify="center")
        self.enter_disks.insert(0, str(self.max_disks))
        self.enter_disks.pack(side=LEFT, padx=10)

        # Buttons
        self.make_control_button("START", self.auto)
        self.make_control_button("STOP", self.stop)
        self.make_control_button("PREV", self.previous_step)
        self.make_control_button("NEXT", self.next_step)
        self.make_control_button("RESET", self.generate)

        # -----------------------------
        # Hanoi state
        # -----------------------------
        self.state = 0
        self.num_disks = self.max_disks
        self.states = []
        self.auto_running = False

        self.generate()

    # -----------------------------
    # Helper to create buttons in control frame
    # -----------------------------
    def make_control_button(self, text, command):
        btn = Button(
            self.control_frame,
            text=text,
            font=self.ui_font,
            bg="#9b8cff",
            fg="white",
            relief="flat",
            padx=15,
            pady=5,
            command=command
        )
        btn.pack(side=LEFT, padx=5)

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
        y = self.canvas_height - self.base_height - self.disk_height * len(stacks[i])

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
        # Clear canvas items but keep background separate
        self.canvas.delete("all")
        self.canvas.create_image(0, 0, image=self.bg_img, anchor="nw")
        
        self.draw_base()
        state = self.states[self.state]
        for i in range(3):
            self.draw_stack(i, state)

        # Moves counter
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
        self.root.after(self.delay, self.auto_step)

    def auto(self):
        self.auto_running = True
        self.root.after(self.delay, self.auto_step)

    def stop(self):
        self.auto_running = False

# -----------------------------
# Run program
# -----------------------------
if __name__ == "__main__":
    root = Tk()
    TowerOfHanoiGUI(root)
    root.mainloop()