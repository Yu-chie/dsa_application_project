# AlgoCraft: Data Structures & Algorithms Application Suite
> **BSCPE 2-6 | Academic Year 2025-2026**

AlgoCraft is a Python-based graphical application suite developed to demonstrate the practical implementation of fundamental Data Structures and Algorithms. Through interactive simulations and real-time visualizations, this project bridges the gap between theoretical DSA concepts and functional software logic.

---

## 🛠️ Data Structures & Logic Applied

### 1. Stack (LIFO) - Parking Garage Simulator
Implemented in `stack_logic.py`, this module simulates a narrow parking lane.
* **Mechanism:** Uses a Python list as a Stack where cars are "Pushed" (Parked) and "Popped" (Departed).
* **Specific Removal:** Includes a "Shuffle Pop" algorithm where cars above a target are moved to a temporary stack and then returned, simulating real-world garage maneuvers.

### 2. Queue (FIFO) - Managed Parking System
Implemented in `parking_garage.py`, this features a more complex queuing system.
* **Mechanism:** Manages a "Waiting Area" for cars when the garage is full.
* **Game Logic:** To remove a car from the middle of the garage, cars in front must temporarily exit and re-join at the rear of the line, demonstrating how order is preserved in a sequential queue structure.

### 3. Binary Tree (BT) - Traversal Visualizer
Implemented in `bt_main.py`, this module allows users to build custom trees.
* **Traversals:** Supports real-time calculation of **Preorder (TLR)**, **Inorder (LTR)**, and **Postorder (LRT)** paths.
* **Visualization:** Dynamically draws nodes and edges based on user-defined levels (up to 5).

### 4. Binary Search Tree (BST) - Efficient Sorting
Implemented in `bst_main.py`, this focuses on sorted data organization.
* **Property:** Ensures the Left Child < Parent < Right Child property is maintained during insertion.
* **Features:** Supports both manual value input and randomized tree generation, with an **Inorder traversal** display to show the resulting sorted sequence.

### 5. Recursion - Tower of Hanoi Solver
Implemented in `hanoi_logic.py`, this solves the classic mathematical puzzle.
* **Recursive Algorithm:** Implements the $2^n - 1$ moves logic to solve the puzzle for 7-9 disks.
* **GUI Visualization:** Provides an automated "Auto-Solve" playback and step-by-step navigation (Next/Prev) to visualize the recursive stack.

---

## ✨ Key Features
* **Interactive GUIs:** Built with `tkinter`, providing a user-friendly way to interact with abstract data structures.
* **Real-time Feedback:** Visual logs and transaction tables (using `ttk.Treeview`) track every move in the parking simulations.
* **Dynamic Visualization:** Trees and puzzles are drawn dynamically on `tk.Canvas` based on user input.

---

## 👥 Collaborators
* **Cas, Maria Kristina L.** - Binary Tree and Binary Search Tree
* **Ilano, Victoria Yuki M.** - Queue
* **Rivera, Chloie Nichole L.** - Recursion
* **Vasques, John Carlo R.** - Stack
