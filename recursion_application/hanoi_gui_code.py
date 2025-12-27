from tkinter import *
import tkinter.messagebox as messagebox

class TowerOfHanoiGUI:
    def __init__(self, master):
        '''
        Initialize the Tower of Hanoi GUI application.
        '''
        # Options
        self.title = "Recursion: Tower of Hanoi"
        self.delay = 500
        self.max_disks = 7
        self.canvas_width = 500
        self.canvas_height = 300
        self.disk_height = 20
        self.disk_width_increment = 14
        self.base_height = 50
        self.base_color = "#985f28"
        self.stack_width = 10
        self.stack_height = 200
        self.space_between_stacks = 100
        self.colors = ["#ef476f", "#f78c6b", "#ffd166", "#06d6a0", "#118ab2", "#073b4c"]

        # Create main window
        master.resizable(False, False)
        master.title(self.title)
        self.root = master

        # Create toolbar
        self.toolbar = Frame(master, relief=RAISED)
        self.toolbar.pack(side=TOP, fill=X)

        # Create canvas
        self.canvas = Canvas(width=self.canvas_width, height=self.canvas_height, bg="white")
        self.canvas.pack()

        # Add label for entry field
        Label(self.toolbar, text="Number of disks (5-7): ").pack(side=LEFT)

        # Create entry field for number of disks
        self.enter_disks = Entry(self.toolbar, width=7)
        self.enter_disks.pack(side=LEFT)
        self.enter_disks.insert(0, str(self.max_disks))

        # Add buttons to toolbar
        Button(self.toolbar, text="Reset", command=self.generate).pack(side=RIGHT)
        Button(self.toolbar, text="Next Step", command=self.next_step).pack(side=RIGHT)
        Button(self.toolbar, text="Previous Step", command=self.previous_step).pack(side=RIGHT)
        Button(self.toolbar, text="Stop", command=self.stop).pack(side=RIGHT)  # Now self.stop exists
        Button(self.toolbar, text="Start", command=self.auto).pack(side=RIGHT)  # Now self.auto exists

        # Nothing has been generated yet
        self.state = 0
        self.num_disks = self.max_disks
        self.states = []  # Fixed: Was self.state = [] (typo)
        self.auto_running = False

        # Draw the towers
        self.generate()

    def move(self, number, stack_from, stack_to):  # Renamed from the misplaced "generate"
        '''
        Recursive method to move the disks.
        '''
        # Base case: one item to move
        if number == 1:
            self.stacks[stack_to].append(self.stacks[stack_from].pop())
            self.states.append([[j for j in self.stacks[i]] for i in range(3)])

        # Recursive case: more than one item to move
        else:
            aux_stack = 3 - stack_from - stack_to
            self.move(number - 1, stack_from, aux_stack)
            self.move(1, stack_from, stack_to)
            self.move(number - 1, aux_stack, stack_to)

    def hanoi(self, size):
        '''
        Method to generate the Tower of Hanoi states.
        '''
        # Generate the stacks
        self.stacks = [[] for _ in range(3)]
        self.stacks[0] = [size - i for i in range(size)]

        # Save initial state
        self.states = [[[j for j in self.stacks[i]] for i in range(3)]]

        # Move the stack and return list of states
        self.move(size, 0, 2)  # Now calls the renamed self.move
        return self.states

        def generate(self):  # The proper GUI reset method (no longer conflicting)
        '''
        Generate the states and draw the first state.
        '''
        try:
            entered = int(self.enter_disks.get())
            if entered < 5 or entered > 7:
                messagebox.showerror("Invalid Input", "Number of disks must be between 5 and 7.")
                self.num_disks = self.max_disks  # Reset to default (7)
                self.enter_disks.delete(0, END)  # Clear the entry field
                self.enter_disks.insert(0, str(self.max_disks))  # Re-insert default
                return  # Do not proceed with generation
            self.num_disks = entered
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number between 5 and 7.")
            self.num_disks = self.max_disks  # Reset to default
            self.enter_disks.delete(0, END)
            self.enter_disks.insert(0, str(self.max_disks))
            return  # Do not proceed

        self.state = 0
        self.states = self.hanoi(self.num_disks)  # Call the embedded logic
        self.draw_current_state()
        
    def previous_step(self):
        '''
        Go back to previous state.
        '''
        self.state -= 1
        if self.state < 0:
            self.state = len(self.states) - 1
        self.draw_current_state()

    def next_step(self):
        '''
        Advance the state by one.
        '''
        self.state = (self.state + 1) % len(self.states)
        self.draw_current_state()

    def get_stack_coordinate(self, stack_num):
        '''
        Return the x-coordinate of one of the stacks
        (the coordinate is the coordinate of the left side
        of its 'post'/'rod')

        With width x, we have
        1/6 * x | 1/3 * x | 1/3 * x | 1/6 * x
        so that each rod has the same amount of space
        '''
        return (self.canvas_width // 3) * stack_num + (self.canvas_width // 6)

    def draw_base(self):
        '''
        Draw the base (the empty stacks)
        '''
        # Draw the bottom
        self.canvas.create_rectangle(
            0, self.canvas_height - self.base_height, self.canvas_width, self.canvas_height,
            outline=self.base_color,
            fill=self.base_color
        )

        # Draw the three stacks
        for i in range(3):
            start_x = self.get_stack_coordinate(i)  # get the starting x-coordinate

            self.canvas.create_rectangle(
                start_x, self.canvas_height - self.base_height - self.stack_height, start_x + self.stack_width, self.canvas_height - self.base_height,
                outline=self.base_color,
                fill=self.base_color
            )

    def draw_stacks(self, stack_num, current_stacks):  # Renamed for consistency (was draw_stack in original)
        '''
        Draw one of the stacks
        '''
        # Find the center of the post
        center = self.get_stack_coordinate(stack_num) + (self.stack_width // 2)

        # Get the starting y-coordinate
        y = self.canvas_height - self.base_height - (self.disk_height * len(current_stacks[stack_num]))

        # Draw each disk in the stack
        for index in range(len(current_stacks[stack_num])):
            value = current_stacks[stack_num][::-1][index]  # get the disk's value

            width = self.disk_width_increment * value + self.disk_width_increment  # calculate the disk's width

            self.canvas.create_rectangle(
                center - (width // 2), y, center + (width // 2), y + self.disk_height,
                fill=self.colors[(value - 1) % len(self.colors)]
            )

            y += self.disk_height  # increment y for next disk

    def draw_current_state(self):
        '''
        Draw current state.
        '''
        self.canvas.delete(ALL)  # clear the canvas
        self.draw_base()  # draw the base
        to_draw = self.states[self.state]  # get the state to draw

        for i in range(3):
            self.draw_stacks(i, to_draw)  # draw each stack

        # Draw move counter
        self.canvas.create_text(self.canvas_width // 2, self.canvas_height - (self.base_height // 2), text=f"Moves: {self.state}")

    def auto_step(self):
        '''
        Step through the solution with a time delay.
        '''
        # Stop if done or stopped
        if self.state == len(self.states) - 1 or not self.auto_running:
            self.auto_running = False
            return

        # Advance one step
        self.next_step()

        # Delay before next step
        self.root.after(self.delay, self.auto_step)

    def auto(self):  # Moved to class level (was indented under auto_step)
        '''
        Start auto-solving.
        '''
        self.auto_running = True
        self.root.after(self.delay, self.next_step)
        self.root.after(2 * self.delay, self.auto_step)  # Adjusted delay for better timing

    def stop(self):  # Moved to class level (was indented under auto_step)
        '''
        Stop auto-solving.
        '''
        self.auto_running = False

# Main program execution
root = Tk()
window = TowerOfHanoiGUI(root)
root.mainloop()
