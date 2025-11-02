"""
-------------------------------------------------------------------
Name: JAYESH JADHAV
PRN: 202301040019
Problem Statement: Implement and compare all types of AI searching algorithms 
(State Space Search) with example (Maze and other problems)
-------------------------------------------------------------------
"""

# ===============================================================
# 🧠  STATE SPACE SEARCH - COMPREHENSIVE IMPLEMENTATION IN PYTHON
# ===============================================================

# Each section implements one category of search algorithms with comments,
# explanations, and a brief analysis of time/space complexity.

# 1️⃣ UNINFORMED SEARCH — BFS and DFS in a Maze

from collections import deque
import heapq
import random
import math

maze = [
    ['S', '.', '.', '#', '.', '.', '.'],
    ['#', '#', '.', '#', '.', '#', '.'],
    ['.', '.', '.', '.', '.', '#', '.'],
    ['.', '#', '#', '#', '.', '.', 'G']
]

rows, cols = len(maze), len(maze[0])
directions = [(1,0), (-1,0), (0,1), (0,-1)]  # Down, Up, Right, Left


def print_maze(maze):
    for r in maze:
        print(' '.join(r))
    print()


def reconstruct_path(visited, end):
    path = []
    while end:
        path.append(end)
        end = visited[end]
    return path[::-1]


def bfs(start):
    """Breadth-First Search (Level-wise, Optimal for uniform cost)"""
    queue = deque([start])
    visited = {start: None}
    while queue:
        x, y = queue.popleft()
        if maze[x][y] == 'G':
            return reconstruct_path(visited, (x, y))
        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != '#' and (nx, ny) not in visited:
                visited[(nx, ny)] = (x, y)
                queue.append((nx, ny))
    return None


def dfs(start):
    """Depth-First Search (Can get stuck in deep branches)"""
    stack = [start]
    visited = {start: None}
    while stack:
        x, y = stack.pop()
        if maze[x][y] == 'G':
            return reconstruct_path(visited, (x, y))
        for dx, dy in directions:
            nx, ny = x+dx, y+dy
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != '#' and (nx, ny) not in visited:
                visited[(nx, ny)] = (x, y)
                stack.append((nx, ny))
    return None


print("==== UNINFORMED SEARCH ====")
print_maze(maze)
print("BFS Path:", bfs((0, 0)))
print("DFS Path:", dfs((0, 0)))
print("BFS => Time: O(b^d), Space: O(b^d)")
print("DFS => Time: O(b^m), Space: O(bm)")
print("\n")

# 2️⃣ INFORMED SEARCH — A* Algorithm (Heuristic = Manhattan Distance)

def heuristic(a, b):
    """Heuristic: Manhattan distance"""
    return abs(a[0]-b[0]) + abs(a[1]-b[1])

def reconstruct_path(came_from, current):
    """Helper: Reconstruct the path from goal to start"""
    path = [current]
    while current in came_from:
        current = came_from[current]
        path.append(current)
    return path[::-1]  # reverse to start→goal

def a_star(start, goal):
    """A* Search uses f(n) = g(n) + h(n)"""
    open_set = [(0, start)]      # priority queue → stores (f(n), node)
    g_score = {start: 0}         # cost from start to current node
    came_from = {}               # to reconstruct path later

    while open_set:
        _, current = heapq.heappop(open_set)
        
        # ✅ If we reached the goal — reconstruct and return path
        if current == goal:
            return reconstruct_path(came_from, current)
        
        # Explore all 4 directions
        for dx, dy in directions:
            nx, ny = current[0]+dx, current[1]+dy
            
            # ✅ Valid next position
            if 0 <= nx < rows and 0 <= ny < cols and maze[nx][ny] != '#':
                tentative_g = g_score[current] + 1  # uniform cost = 1
                
                # If new path is better or new node found
                if (nx, ny) not in g_score or tentative_g < g_score[(nx, ny)]:
                    g_score[(nx, ny)] = tentative_g
                    f = tentative_g + heuristic((nx, ny), goal)
                    heapq.heappush(open_set, (f, (nx, ny)))
                    came_from[(nx, ny)] = current  # ✅ Store parent for path reconstruction
    
    return None  # if no path found

# ✅ Now test A*
print("==== INFORMED SEARCH (A*) ====")
path_a = a_star((0, 0), (3, 6))
if path_a:
    print("A* Path:", path_a)
else:
    print("No path found using A*")
print("A* => Time: O(b^d), Space: O(b^d), Optimal if heuristic is admissible\n")


# 3️⃣ CONSTRAINT SATISFACTION PROBLEM — Map Coloring Example

print("==== CONSTRAINT SATISFACTION (Map Coloring) ====")

colors = ['Red', 'Green', 'Blue']
neighbors = {
    'A': ['B', 'C'],
    'B': ['A', 'C', 'D'],
    'C': ['A', 'B', 'D'],
    'D': ['B', 'C']
}

def is_valid(node, color, assignment):
    for n in neighbors[node]:
        if n in assignment and assignment[n] == color:
            return False
    return True

def backtrack(assignment):
    if len(assignment) == len(neighbors):
        return assignment
    node = [n for n in neighbors if n not in assignment][0]
    for color in colors:
        if is_valid(node, color, assignment):
            assignment[node] = color
            result = backtrack(assignment)
            if result:
                return result
            assignment.pop(node)
    return None

solution = backtrack({})
print("Map Coloring Solution:", solution)
print("CSP => Time: O(b^d), Space: O(d)\n")

# 4️⃣ LOCAL SEARCH — Hill Climbing Example (Maximize a function)

print("==== LOCAL SEARCH (Hill Climbing) ====")

def objective(x):
    return x * math.sin(10 * math.pi * x) + 1.0  # Function to maximize

def hill_climb():
    x = random.uniform(0, 1)
    step_size = 0.01
    for _ in range(1000):
        new_x = x + random.uniform(-step_size, step_size)
        if 0 <= new_x <= 1 and objective(new_x) > objective(x):
            x = new_x
    return x, objective(x)

x_best, y_best = hill_climb()
print(f"Hill Climbing Result: x={x_best:.4f}, f(x)={y_best:.4f}")
print("Local Search => Time: O(iterations), Space: O(1)\n")

# 5️⃣ ADVERSARIAL SEARCH — MiniMax (Tic-Tac-Toe 1-move Example)

print("==== ADVERSARIAL SEARCH (MiniMax) ====")

def minimax(depth, is_maximizing):
    if depth == 0:
        return random.randint(-10, 10)  # Random terminal value
    if is_maximizing:
        best = -float('inf')
        for _ in range(2):  # Two possible moves
            value = minimax(depth - 1, False)
            best = max(best, value)
        return best
    else:
        best = float('inf')
        for _ in range(2):
            value = minimax(depth - 1, True)
            best = min(best, value)
        return best

score = minimax(3, True)
print("MiniMax Decision Score:", score)
print("Adversarial Search => Time: O(b^m), Space: O(m)\n")

# 6️⃣ GENETIC ALGORITHM — Optimize f(x) = x² in [0,31]

print("==== GENETIC ALGORITHM ====")

def fitness(x):
    return x*x  # Our goal is to maximize this

def genetic_algorithm():
    population = [random.randint(0, 31) for _ in range(6)]
    for generation in range(10):
        population = sorted(population, key=lambda x: -fitness(x))
        next_gen = population[:2]  # Keep best two
        while len(next_gen) < 6:
            p1, p2 = random.sample(population[:4], 2)
            child = (p1 + p2)//2  # Crossover
            if random.random() < 0.1:  # Mutation
                child ^= 1
            next_gen.append(child)
        population = next_gen
    return max(population, key=fitness)

best = genetic_algorithm()
print("Genetic Algorithm Best Solution:", best, "Fitness:", fitness(best))
print("GA => Time: O(generations * population), Space: O(population)\n")

print("==== COMPARISON SUMMARY ====")
print("""
1. Uninformed Search — BFS, DFS
   ▪ Time: BFS O(b^d), DFS O(b^m)
   ▪ Space: BFS O(b^d), DFS O(bm)
   ▪ BFS optimal for uniform cost.

2. Informed Search — A*
   ▪ Uses heuristic h(n)
   ▪ Time & Space: O(b^d)
   ▪ Optimal if h(n) is admissible.

3. CSP — Constraint Satisfaction
   ▪ Solves assignment-based problems.
   ▪ Time: O(b^d)
   ▪ Space: O(d)

4. Local Search — Hill Climbing
   ▪ Works on continuous functions.
   ▪ Time: O(iterations)
   ▪ Space: O(1)

5. Adversarial Search — MiniMax
   ▪ Used in two-player games.
   ▪ Time: O(b^m)
   ▪ Space: O(m)

6. Genetic Algorithm
   ▪ Evolution-based stochastic optimization.
   ▪ Time: O(generations × population)
   ▪ Space: O(population)
""")
