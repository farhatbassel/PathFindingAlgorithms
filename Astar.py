import pygame 
from queue import PriorityQueue

# Setting up the size of the box
WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* finding algorithm")

# Colors we are going to use 

RED = (255,0,0)             # Not a correct path
GREEN = (0,225,0)           # Lowest current f
WHITE = (255,255,255)       # Not visited yet
BLACK = (0,0,0)             # Obstacle
PURPLE = (128,0,128)        # Fastest way
ORANGE = (255,165,0)        # Start node
TURQUOISE = (64,224,208)    # End node
GREY = (128,128,128)        # Grid lines


class Node:
    """
    This class definies each point in the grid
    """
    def __init__(self, row, col, width, total_rows):
       self.row = row
       self.col = col
       self.x = row * width
       self.y = col * width
       self.total_rows = total_rows
       self.color = WHITE
       self.width = width
       
    def get_pos(self):
        """

        Returns
        -------
        The (y,x) values of the node position

        """
        return self.row, self.col
     
    # These functions are used to color the nodes
    def is_barrier(self):                       
        return self.color == BLACK
     
    def reset(self):                         
        self.color = WHITE                  
    
    def change_color(self, new_color):
        self.color = new_color
    
    # This function is used to draw the nodes, it can be the path, blockers
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))
        
    # Getting the nieghbors of each node
    def update_neighbors(self,grid):
        self.neighbors = []

        if self.row > 0  and not grid[self.row - 1][self.col].is_barrier(): #UP
            self.neighbors.append(grid[self.row - 1][self.col])
            
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): #RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
            
        if self.col > 0  and not grid[self.row][self.col - 1].is_barrier(): #LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
        
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

            
def reconstruct_path(came_from, current, draw):
    """
    

    Parameters
    ----------
    came_from : Dictionary
        The nodes taken to reach the current path
    current : Node
        The node we want to look at
    draw : function
        Draws the path

    Returns
    -------
    A line that draws through the came_from dictionary

    """
    
    while current in came_from:
        current = came_from[current]
        current.change_color(PURPLE)
        draw()
        
def algorithm(draw, grid, start, end):
    
    """
    Parameters
    ----------
    draw : function
        Draws the path
    grid : 2D list
        The full grid we are working in
    start : Node
        The node we start at
    end : Node
        The node we want to reach

    """
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    came_from = {}
    
    # We fill g with inf at the beginning
    g_score = {node: float('inf') for row in grid for node in row}
    g_score[start] = 0
    
    # f = g + hwe also fill f with inf except the start node that has h
    f_score = {node: float('inf') for row in grid for node in row}
    f_score[start] = h(start.get_pos(),end.get_pos())
    
    open_set_hash = {start}
    
    while not open_set.empty():
        for event in pygame.event.get():            # This is added if want
            if event.type == pygame.QUIT:           # to leave the animation 
                pygame.quit()                       # before it ends
                
        
        # If we have a tie between two nodes take the first one
        current = open_set.get()[2]
        open_set_hash.remove(current)
        
        # Once we reach the end node, reconstruct the fastest path used 
        # to reach it
        if current == end:
            reconstruct_path(came_from, end, draw)
            end.change_color(TURQUOISE)
            return True
        
        for neighbor in current.neighbors:
            temp_g_score = g_score[current] + 1 
            
            if temp_g_score < g_score[neighbor]:
                came_from[neighbor] = current
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    neighbor.change_color(GREEN)
                    
        draw()
        
        if current != start:
            current.change_color(RED)
            
    return False
           
def h(p1,p2):
    
    """
    The heuristic function h(x).
    
    Parameters
    ----------
    p1: node
    p2: node

    Returns
    -------
    
    The fastest path that isn't diagonal 
    """
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)
        
def make_grid(rows,width):
    
    """
    The heuristic function we use.
    
    Parameters
    ----------
    rows: int
        Number of rows we want to implement
    width: int
        Width we want to implement
    Returns
    -------
    
    A two dimensional grid that is fully contained with white nodes 
    """
    gap = width // rows
    
    return [[Node(i,j,gap,rows) for j in range(rows)] for i in range(rows)]
    
        
def draw_grid(win,rows,width):
    
    """
    The heuristic function we use.
    
    Parameters
    ----------
    rows: int
        Number of rows we want to implement
    width: int
        Width we want to implement
    Returns
    -------
    
    Draws the grid
    """
    gap = width // rows
    
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(win, GREY, (j*gap, 0), (j*gap,width))
        
        
def draw(win,grid,rows,width):
    """
    

    Parameters
    ----------
    win : window
        The window we created using pygame
    grid : 2D nested list
        The grid we are using
    rows : int
        Number of rows we want to implement
    width : int
        Width we want to implement

    Returns
    -------
    Draws on the windows the nodes and the grid, while filling the nodes in 
    white

    """
    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)
    
    draw_grid(win, rows, width)
    pygame.display.update()
    
def get_clicked_pos(pos, rows, width):
    """
    
    Find the position where we clicked with the mouse
    
    Parameters
    ----------
    pos : node
        Position of the mouse
    rows : int
        Number of rows we want to implement
    width : int
        Width we want to implement

    Returns
    -------
    rows : int
    col : int
        Position of the mouse in (y,x) coords

    """
    gap = width // rows
    y, x = pos

    rows = y // gap
    col = x // gap

    return rows, col

def main(win, width):
    # Number of rows we want the bigger the slower
    ROWS = 100      
    grid = make_grid(ROWS, width)
    
    start = None
    end = None
    run = True
    
    while run:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():            # To exit the game
            if event.type == pygame.QUIT:
                run = False
            
            if pygame.mouse.get_pressed()[0]:       # Left Mouse
                pos = pygame.mouse.get_pos()
                rows, col = get_clicked_pos(pos, ROWS, width)
                node = grid[rows][col]
                
                if not start and node != end:       # Setting the start node
                    start = node
                    start.change_color(ORANGE)
                    
                elif not end and node !=start:      # Setting the end node
                    end = node
                    end.change_color(TURQUOISE)
                    
                elif node != end and node !=start:  # Setting obstacles
                    node.change_color(BLACK)
                
            elif pygame.mouse.get_pressed()[2]:     # Right Mouse
                pos = pygame.mouse.get_pos()
                rows, col = get_clicked_pos(pos, ROWS, width)
                node = grid[rows][col]
                node.reset()                        # Reseting node to white
                
                if node == start:
                    start = None
                elif node == end:
                    end = None
            
            if event.type == pygame.KEYDOWN:        # Space to begin
                if event.key == pygame.K_SPACE:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                        
                    algorithm(lambda: draw(win, grid, ROWS, width), grid, start, end)
                    
                if event.key == pygame.K_c:         # C to clear
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)
                    
    pygame.quit()
        
main(WIN,WIDTH)
        
        
        
        
        
        
        
        
        
        
        
        
