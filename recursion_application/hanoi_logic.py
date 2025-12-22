'''
Tower of Hanoi Solver
This script provides a solution to the Tower of Hanoi problem using recursion.
Pseudocode:

Use class TowerofHanoi for solving the Tower of Hanoi problem.
// Construction: Initialize with number of disks
// Recursive funtion to move disks from one stack to another
// Method to solve the puzzle and return all states
// Main function to execute the solver with user input
'''

class TowerOfHanoi:
    def __init__(self, size):
        self.size = size
        self.stacks = {[] for _ in range(3)}
        self.stacks[0] = [size - i for i in range(size)]                      #largest disk at bottom
        self.states = {[(j for j in self.stacks[i])] for i in range(3)}       #to save initial state

    def move_disks(self, number, stack_from, stack_to):
        if number == 1: #base case
            self.stacks[stack_to].append(self.stacks[stack_from].pop())
            self.states.append([[j for j in self.stacks[i]] for i in range(3)])
        else: #recursive case
            aux_stack = 3 - stack_from - stack_to
            self.move_disks(number - 1, stack_from, aux_stack)
            self.move_disks(1, stack_from, stack_to)
            self.move_disks(number - 1, aux_stack, stack_to)