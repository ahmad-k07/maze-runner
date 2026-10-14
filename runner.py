from maze import get_dimensions, get_walls
from typing import Optional

def create_runner(x: int = 0, y: int = 0, orientation: str = "N"):
    """
    Creates the runner with a start position and orientation
    The default starting position and orientation are (0,0), North
    Parameters: x, y (integers), orientation (str like "N", "E", "S", "W")
    Returns: runner dictionary with position (x and y) and orientation
    """
    #using a dictionary to store the runners information, as it's a key-value
    #it holds x, y, and which way they are facing (their orientation)
    runner = {
        "x_coordinate": x,
        "y_coordinate": y,
        "orientation": orientation
    }
    return runner

def get_x(runner: dict):
    """
    Finds the x coordinate of the runner
    Using the dictionary made in create_runner
    Parameter: runner
    Returns: integer value of the x coordinate
    """
    return runner["x_coordinate"]

def get_y(runner: dict):
    """
    Gets the y coordinate of the runner
    Uses the dictionary in create_runner
    Parameter: runner
    Returns: integer value of the y coordinate
    """
    return runner["y_coordinate"]

def get_orientation(runner: dict):
    """
    Finds which way the runner is facing/ the orientation
    Using the dictionary in create_runner
    Parameter: runner
    Returns: orientation value, either: N, E, S, W, which is a string
    """
    return runner["orientation"]

def turn(runner: dict, direction: str):
    """
    Turns the runner left or right
    Changes orientation but keeps the same position
    Parameters: runner and direction, either "Left" or "Right"
    Returns: the updated runner dictionary
    """
    if direction == "Left":
        #check current direction and turns left to that specific direction
        if runner["orientation"] == "N":
            runner["orientation"] = "W"
        elif runner["orientation"] == "E":
            runner["orientation"] = "N"
        elif runner["orientation"] == "S":
            runner["orientation"] = "E"
        elif runner["orientation"] == "W":
            runner["orientation"] = "S"

    elif direction == "Right":
        #check current direction and turns right
        if runner["orientation"] == "N":
            runner["orientation"] = "E"
        elif runner["orientation"] == "E":
            runner["orientation"] = "S"
        elif runner["orientation"] == "S":
            runner["orientation"] = "W"
        elif runner["orientation"] == "W":
            runner["orientation"] = "N"

    return runner


def forward(runner: dict):
    """
    Makes the runner move forward by one
    Changes x or y depending on which way they face/orientation
    Parameter: runner
    Returns: updated runner dictionary (either x or y changes)
    """
    if runner["orientation"] == "N":
        #north is up, so runner goes up by 1, increasing y
        runner["y_coordinate"] += 1
    elif runner["orientation"] == "E":
        #east is right, so increase x as runner moves along
        runner["x_coordinate"] += 1
    elif runner["orientation"] == "S":
        #opposite of north
        runner["y_coordinate"] -= 1
    elif runner["orientation"] == "W":
        #opposite of east
        runner["x_coordinate"] -= 1

    return runner

def sense_walls(runner: dict, maze: list[any]) -> tuple[bool, bool, bool]:
    """
    Checks for walls relative to the runner which are left, front, right
    It translates map directions (N,E,S,W) to runner views
    Parameters: runner and maze
    Returns: tuple of booleans left wall, front wall, right wall
    """
    x = get_x(runner)
    y = get_y(runner)
    orientation = get_orientation(runner)

    #get the walls for the current cell
    north, east, south, west = get_walls(maze, x, y)

    #map the wall variables to their string keys
    wall = {
        "N": north,
        "E": east,
        "S": south,
        "W": west
    }

    #define what is left, front, and right for each direction
    #by creating a dictionary with tuples as the values
    direction = {
        "N": ("W", "N", "E"),
        "E": ("N", "E", "S"),
        "S": ("E", "S", "W"),
        "W": ("S", "W", "N")
    }

    #get the actual compass directions for left, front, right
    left, front, right = direction[orientation]

    #return the wall boolean value for those directions, like False, True
    return (wall[left], wall[front], wall[right])

def go_straight(runner: dict, maze: list[any]):
    """
    Moves the runner forward by one cell
    But checks for a wall first to prevent crashing
    Parameters: runner and maze
    Returns: the updated runner or raises an error if there is a wall in front
    """
    #check if there is a wall in front of the runner
    left_wall, front_wall, right_wall = sense_walls(runner, maze)

    if front_wall:
        #since there is a wall in front raise a value error
        #runner doesn't move
        raise ValueError("There is a wall in front")
    return forward(runner)

def move(runner: dict, maze: list[any], visited_counts: dict) -> tuple[dict, str]:
    """
    Decides the next move using Trémaux's algorithm (DFS)
    It prioritizes cells that have been visited the least amount of times
    Parameters: runner, maze, and the dictionary of visited counts
    Returns: updated runner and the movement action string (e.g. "F", "LF")
    """
    current_x = get_x(runner)
    current_y = get_y(runner)
    orientation = get_orientation(runner)

    #get walls for the current position
    #north, east, south, west are booleans (True if there is a wall)
    north, east, south, west = get_walls(maze, current_x, current_y)
    
    #define coordinate changes for each compass direction
    #N adds 1 to y, E adds 1 to x, S minus 1 from y
    directions = {
        "N": (0, 1),
        "E": (1, 0),
        "S": (0, -1),
        "W": (-1, 0)
    }

    #map walls to directions to check if runner can move
    walls = {"N": north, "E": east, "S": south, "W": west}

    #list to store possible moves as tuples: (visit_count, direction_key)
    possible_moves = []

    for direction_key, (dx, dy) in directions.items():
        #only check if there is no wall
        if not walls[direction_key]:
            #calculate the neighbor's coordinates
            nx, ny = current_x + dx, current_y + dy
            
            #get the visit count for the neighbor, default to 0 if not visited
            count = visited_counts.get((nx, ny), 0)
            
            #add to list of options
            possible_moves.append((count, direction_key))

    #sort the moves:
    # First by visit count (lowest first, so we explore new areas)
    # Then by a simple tie-breaker (just keeps it consistent)
    possible_moves.sort(key=lambda x: x[0])

    #pick the best direction (the one with lowest visits)
    best_direction = possible_moves[0][1]

    #determine the action needed to face the best direction
    #compare current orientation with the best_direction
    
    action = ""
    
    #logic to decide turns based on orientation and target direction
    if orientation == best_direction:
        #already facing the right way
        runner = go_straight(runner, maze)
        action = "F"
        
    elif (orientation == "N" and best_direction == "W") or \
         (orientation == "W" and best_direction == "S") or \
         (orientation == "S" and best_direction == "E") or \
         (orientation == "E" and best_direction == "N"):
        #need to turn left once
        runner = turn(runner, "Left")
        runner = go_straight(runner, maze)
        action = "LF"
        
    elif (orientation == "N" and best_direction == "E") or \
         (orientation == "E" and best_direction == "S") or \
         (orientation == "S" and best_direction == "W") or \
         (orientation == "W" and best_direction == "N"):
        #need to turn right once
        runner = turn(runner, "Right")
        runner = go_straight(runner, maze)
        action = "RF"
        
    else:
        #the direction is behind runner (180 degrees)
        #turn right twice to face back, then move forward
        runner = turn(runner, "Right")
        runner = turn(runner, "Right")
        runner = go_straight(runner, maze)
        action = "B"

    return runner, action

def explore(runner: dict, maze: list[any], goal: Optional[tuple[int, int]]) \
        -> list[tuple[int, int, str]]:
    """
    Allow runner to explore maze using the Trémaux algorithm
    It remembers how many times it visited each cell to make smart moves
    More effective than left hug algorithm
    Parameters: runner, maze, and goal
    Returns: list of (x, y, action) for the whole path
    """
    movement = []
    
    #dictionary to store how many times we visited a coordinate
    #key is (x, y), value is the count (integer)
    visited_counts = {}

    #if goal is None, set goal/target position to top right corner
    if goal is None:
        width, height = get_dimensions(maze)
        x_goal, y_goal = width - 1, height - 1
    else:
        x_goal, y_goal = goal

    #mark the starting position as visited (count = 1)
    start_x = get_x(runner)
    start_y = get_y(runner)
    visited_counts[(start_x, start_y)] = 1

    #keep moving until the runner's coordinates match the goal
    while get_x(runner) != x_goal or get_y(runner) != y_goal:
        current_x = get_x(runner)
        current_y = get_y(runner)

        # if the visited_counts is passed, runner knows where it is
        runner, action = move(runner, maze, visited_counts)
        
        #get the new position after the move
        new_x = get_x(runner)  
        new_y = get_y(runner)
        
        #update the visit count for the new position
        #if it was 0, it becomes 1. If it was 1, it becomes 2.
        current_count = visited_counts.get((new_x, new_y), 0)
        visited_counts[(new_x, new_y)] = current_count + 1

        #save the position before the move, and action is done
        movement.append((current_x, current_y, action))

    return movement