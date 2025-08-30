# Vacuum cleaner reflex agent 
# This script simulates a very simple "vacuum cleaner agent"
# operating in a 2D grid world. Each cell is either "Dirty" or "Clean".
# The agent preceives the current cell and acts:
# If the current cell is Dirty - it cleans it.
# Otherwise -> it moves to a neighboring cell.

import random

class environment:

    def __init__(self, size=2):
        """
        Constructor 
        parametres: size(int): the grid will be size x size (default 2x2)

        self.size stores the grid dimension so other methods can use it.
        self.grid builds a nested list (lost of lists) representing rows.
        we use a * nested list comprehension* to fill each cell randomly
        as "Dirty" or "Clean"
        """
        self.size = size # save the grid dimension into the instance 

        # Building a size x size grid
        # Outer list: for each row in ranges(size)
        # Inner list: for each column in range(size)
        # random.random() reutrns a float in [0.0, 1.0]
        # If it's > 0.5, mark the cell as 'Dirty', otherwise 'Clean'
        self.grid = [['Dirty' if random.random() > 0.5 else 'Clean'
                      for _ in range(size)] for _ in range(size)]
        
    def is_dirty(self,x,y):
        """
        Returns true if the cell at coordinates (x,y) is 'Dirty', else false.

        self.grid is a list of rows
        self.grid[x] select the x-th row.
        self.grid[x][y] selects the y-th column in that row.
        """
        return self.grid[x][y] == 'Dirty'
    
    def clean(self,x,y):
        """
        Sets the cell at(x,y) to 'Clean'
        this is a state changing action 
        """
        self.grid[x][y]='Clean'

    def all_clean(self):
        for row in self.grid:
            if 'Dirty' in row:
                return False
            return True

    def display(self):
        """
        Prints the current grid to the console 
        for each row (list of strings), we print it as a Python list,
        so we can visually track which cells are 'Dirty' or 'Clean'
        """
        for row in self.grid: # for-each loop over all rows in the grid
            print(row) # print the row ['Dirty','Clean'...]
        print() # Printing blank line for readability

class VacuumAgent:
    """
    This class represents the agent that moves and cleans.

    Responsibilities:
    - Hold the agent's position (x,y) inside the grid.
    - Perceive the enviroment (check if current cell is dirty)
    - Act based on simple reflex rule:
        If cell is dirty -> clean it.
        else -> move to neighboring cell (u/d/l/r) if possible
    """

    def __init__(self, env:environment):
        """
        Constructor for vacuum agent

        - env (Environment): a reference to the environment the agent operates in.
        """

        self.env = env # Keep a refrence to the environment (compositoon relationship)
        # choose a random starting row (x) and column (y) within bounds
        self.x= random.randint(0, env.size-1)
        self.y= random.randint(0, env.size-1)

    def perceive_and_act(self):
        if self.env.is_dirty(self.x, self.y): # If the cell is dirty...
            # Informative print so we can trace the agent's decision
            print(f"Location ({self.x}, {self.y}) is Dirty -> Cleaning")

            # --- Action phase (cleaning): tell the environment to clean the cell
            self.env.clean(self.x, self.y)
        else:
            # If the cell is already clean we will move to another cell
            # random.choice picks one string from the list of uniformly at random
            direction = random.choice(["UP","DOWN", "LEFT","RIGHT"])

            # we will try to move once based on chosen direction,
            # but only if that move stays inside the grid bounds.
            # Note: row index (x) goes up when we subtract 1, "down" when we add 1.
            # column index (y) goes "left" when we subtract 1, "right" when we add 1.

            # Stores old coordinates so we can report the new loction nicely
            old_x, old_y = self.x, self.y,
            if direction == 'UP' and self.x >0:
                self.x -= 1 # Move one row up (towards index 0)
            elif direction == 'DOWN' and self.x < self.env.size-1:
                self.x += 1 # Move one row down (towards index size-1)
            elif direction == 'LEFT' and self.y >0:
                self.y -= 1 # Move one column left (towards index 0)
            elif direction == 'RIGHT' and self.y < self.env.size - 1:
                self.y += 1 # Move one column right (towards index size-1)
            # If the direction would take us out of bounds, we simply don't move
            # (The agent stays in place or this step.)

            # Print what happened so we can see the chosen direction and new position 
            print(f"Location is clean -> Moving {direction} from ({old_x}, {old_y}) to ({self.x}, {self.y})")

# SIMULATION / PROGRAM DRIVER 
env = environment(size=2)
agent = VacuumAgent(env)

print("Initial Environment:")
env.display()

steps = 0

while not env.all_clean():
    steps +=1
    print(f"Step {steps+1}:")
    agent.perceive_and_act()
    env.display

print(f"All cells are clean after {steps} steps!")
