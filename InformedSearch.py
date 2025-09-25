import heapq
import time
import os

# City map layout
# S = Start (Delivery Boy)
# R = Restaurant
# C = Customer
# # = Blocked Road
# . = Free Road
city = [
    "S...#..",
    "..##..C",
    ".R..#..",
    "...##..",
    "......."
]

ROWS, COLS = len(city), len(city[0])

# Movements: Right, Down, Left, Up
moves = [(0,1),(1,0),(0,-1),(-1,0)]

# ---- Helper functions ----
def find(symbol):
    """Find coordinates of a symbol in the city map"""
    for r in range(ROWS):
        for c in range(COLS):
            if city[r][c] == symbol:
                return (r,c)

start = find("S")
restaurant = find("R")
customer = find("C")

def heuristic(x, y, goal):
    """Manhattan distance heuristic"""
    return abs(x-goal[0]) + abs(y-goal[1])

def is_valid(r,c):
    """Check if cell is within bounds and not blocked"""
    return 0 <= r < ROWS and 0 <= c < COLS and city[r][c] != "#"

def print_city(path=set(), current=None):
    """Prints the city map with path and current position"""
    for r in range(ROWS):
        row_str = ""
        for c in range(COLS):
            if (r,c) == current:
                row_str += "🚴 "  # Delivery boy emoji
            elif (r,c) in path:
                row_str += "* "   # Path marker
            else:
                row_str += city[r][c] + " "
        print(row_str)
    print("\n")

# ---- A* with CSP ----
def a_star_pizza():
    """
    A* search with constraint:
    Delivery boy must collect pizza from Restaurant (R)
    before going to Customer (C).
    """
    # Priority Queue: (f=g+h, g, position, has_pizza, path)
    pq = [(0,0,start,False,[start])]
    visited = set()

    while pq:
        f,g,pos,has_pizza,path = heapq.heappop(pq)

        # Goal condition: reached customer with pizza
        if pos == customer and has_pizza:
            return path

        state = (pos,has_pizza)
        if state in visited:
            continue
        visited.add(state)

        for dr,dc in moves:
            nr,nc = pos[0]+dr,pos[1]+dc
            if not is_valid(nr,nc):
                continue

            new_has_pizza = has_pizza
            if (nr,nc) == restaurant:
                new_has_pizza = True  # Constraint satisfied (pickup pizza)

            # Heuristic changes based on whether we have pizza
            target = customer if new_has_pizza else restaurant
            h = heuristic(nr,nc,target)

            heapq.heappush(pq,(g+1+h,g+1,(nr,nc),new_has_pizza,path+[(nr,nc)]))

    return None

# ---- Run the Game ----
solution = a_star_pizza()

if solution:
    print("✅ Pizza Delivered! Steps followed:\n")

    visited_path = set()
    for step in solution:
        os.system("cls" if os.name == "nt" else "clear")
        visited_path.add(step)
        print_city(path=visited_path, current=step)
        time.sleep(0.5)  # animation speed

    print("🍕 Pizza successfully delivered to the customer!")

else:
    print("❌ Could not deliver pizza. Path blocked!")
