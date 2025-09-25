from collections import deque

# City map
city = [
    "S...#..",
    "..##..C",
    ".R..#..",
    "...##..",
    "......."
]

ROWS, COLS = len(city), len(city[0])
moves = [(0,1),(1,0),(0,-1),(-1,0)]  # Right, Down, Left, Up

def find(symbol):
    for r in range(ROWS):
        for c in range(COLS):
            if city[r][c] == symbol:
                return (r,c)

start = find("S")
restaurant = find("R")
customer = find("C")

def is_valid(r,c):
    return 0 <= r < ROWS and 0 <= c < COLS and city[r][c] != "#"

# ---------------- BFS ----------------
def bfs():
    q = deque([(start, False, [start])])  # (position, has_pizza, path)
    visited = set()

    while q:
        pos, has_pizza, path = q.popleft()

        # Goal condition
        if pos == customer and has_pizza:
            return path

        if (pos,has_pizza) in visited:
            continue
        visited.add((pos,has_pizza))

        for dr,dc in moves:
            nr,nc = pos[0]+dr, pos[1]+dc
            if not is_valid(nr,nc):
                continue

            new_has_pizza = has_pizza
            if (nr,nc) == restaurant:
                new_has_pizza = True

            q.append(((nr,nc), new_has_pizza, path+[(nr,nc)]))
    return None

# ---------------- DFS ----------------
def dfs():
    stack = [(start, False, [start])]
    visited = set()

    while stack:
        pos, has_pizza, path = stack.pop()

        if pos == customer and has_pizza:
            return path

        if (pos,has_pizza) in visited:
            continue
        visited.add((pos,has_pizza))

        for dr,dc in moves:
            nr,nc = pos[0]+dr, pos[1]+dc
            if not is_valid(nr,nc):
                continue

            new_has_pizza = has_pizza
            if (nr,nc) == restaurant:
                new_has_pizza = True

            stack.append(((nr,nc), new_has_pizza, path+[(nr,nc)]))
    return None

# ---------------- Iterative Deepening ----------------
def dls(pos, has_pizza, path, depth, visited):
    if pos == customer and has_pizza:
        return path
    if depth == 0:
        return None

    visited.add((pos,has_pizza))

    for dr,dc in moves:
        nr,nc = pos[0]+dr, pos[1]+dc
        if not is_valid(nr,nc):
            continue
        new_has_pizza = has_pizza
        if (nr,nc) == restaurant:
            new_has_pizza = True

        if (nr,nc,new_has_pizza) not in visited:
            result = dls((nr,nc), new_has_pizza, path+[(nr,nc)], depth-1, visited)
            if result:
                return result
    return None

def ids(max_depth=50):
    for depth in range(max_depth):
        visited = set()
        result = dls(start, False, [start], depth, visited)
        if result:
            return result
    return None

# ---- Run All Searches ----
print("BFS Path:", bfs())
print("DFS Path:", dfs())
print("IDS Path:", ids())
