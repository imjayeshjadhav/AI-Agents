from collections import deque   # Import deque (double-ended queue) for efficient BFS queue operations

# Function to print the current board state
def print_board(board):
    for row in board:               # Iterate through each row of the board
        print(row)                  # Print the row as a list
    print("--------")               # Print a separator for readability

# Function to convert the board into a single string (used for visited set)
def board_to_string(board):
    # Flatten the 2D board into a single string representation
    return ''.join(str(cell) for row in board for cell in row)

# Function to find the blank tile (represented by 0)
def find_blank(board):
    for i in range(3):                  # Iterate through rows
        for j in range(3):              # Iterate through columns
            if board[i][j] == 0:        # Check if cell is blank
                return i, j             # Return its position (row, col)

# Function to swap two tiles and return a new board
def swap(board, x1, y1, x2, y2):
    new_board = [row[:] for row in board]     # Make a deep copy of board
    # Swap values between (x1, y1) and (x2, y2)
    new_board[x1][y1], new_board[x2][y2] = new_board[x2][y2], new_board[x1][y1]
    return new_board                         # Return the new board state

# Function to check if the current board matches the goal board
def is_goal(board, goal):
    return board == goal


# Breadth-First Search with depth limit
def bfs_limited(start, goal, max_depth=20):
    print(f"Breadth First Search (max depth: {max_depth}):")
    
    # Queue stores tuples of (board state, depth)
    q = deque([(start, 0)])
    visited = set()                          # Store visited states
    visited.add(board_to_string(start))      # Mark start as visited
    nodes_explored = 0                       # Counter for explored nodes
    
    # BFS loop
    while q and nodes_explored < 1000:       # Stop if >1000 nodes explored
        current, depth = q.popleft()         # Pop from front (FIFO queue)
        nodes_explored += 1
        
        print(f"Depth {depth}, Nodes explored: {nodes_explored}")
        print_board(current)
        
        if is_goal(current, goal):           # Check if goal reached
            print(f"Goal found in BFS at depth {depth}! Nodes explored: {nodes_explored}\n")
            return True
            
        if depth >= max_depth:               # Skip if we hit max depth
            continue
        
        # Find blank tile to generate neighbors
        x, y = find_blank(current)
        moves = [(1,0), (-1,0), (0,1), (0,-1)]   # Possible moves (down, up, right, left)
        
        for dx, dy in moves:                     # Try each move
            newX, newY = x + dx, y + dy
            if 0 <= newX < 3 and 0 <= newY < 3:  # Check board boundaries
                new_board = swap(current, x, y, newX, newY)   # Swap blank with neighbor
                new_str = board_to_string(new_board)          # Convert to string
                
                if new_str not in visited:       # Only expand if unvisited
                    visited.add(new_str)
                    q.append((new_board, depth + 1))   # Add new state to queue
    
    print(f"Goal not found in BFS within depth {max_depth}. Nodes explored: {nodes_explored}\n")
    return False

# Depth-First Search with depth limit
def dfs_limited(start, goal, max_depth=15):
    print(f"Depth First Search (max depth: {max_depth}):")
    
    # Stack stores tuples of (board state, depth)
    stack = [(start, 0)]
    visited = set()                          # Store visited states
    visited.add(board_to_string(start))      # Mark start as visited
    nodes_explored = 0
    
    # DFS loop
    while stack and nodes_explored < 1000:   # Stop if >1000 nodes explored
        current, depth = stack.pop()         # Pop from back (LIFO stack)
        nodes_explored += 1
        
        print(f"Depth {depth}, Nodes explored: {nodes_explored}")
        print_board(current)
        
        if is_goal(current, goal):           # Check if goal reached
            print(f"Goal found in DFS at depth {depth}! Nodes explored: {nodes_explored}\n")
            return True
            
        if depth >= max_depth:               # Stop expanding if max depth reached
            continue
        
        # Find blank tile to generate neighbors
        x, y = find_blank(current)
        moves = [(1,0), (-1,0), (0,1), (0,-1)]   # Possible moves
        
        for dx, dy in moves:                     # Try each move
            newX, newY = x + dx, y + dy
            if 0 <= newX < 3 and 0 <= newY < 3:  # Check board boundaries
                new_board = swap(current, x, y, newX, newY)
                new_str = board_to_string(new_board)
                
                if new_str not in visited:       # Only expand if unvisited
                    visited.add(new_str)
                    stack.append((new_board, depth + 1))   # Add new state to stack
    
    print(f"Goal not found in DFS within depth {max_depth}. Nodes explored: {nodes_explored}\n")
    return False


if __name__ == "__main__":
    # Define start state
    start = [
        [1, 2, 3],
        [4, 0, 6],
        [7, 5, 8]
    ]
    
    # Define goal state
    goal = [
        [1, 2, 3],
        [4, 5, 6],
        [7, 8, 0]
    ]
    
    print("Start state:")
    print_board(start)
    print("Goal state:")
    print_board(goal)
        
    # Run DFS search with max depth = 10
    bfs_limited(start, goal, max_depth=10)
    # dfs_limited(start, goal, max_depth=10)
