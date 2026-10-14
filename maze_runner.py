import argparse
import sys
from typing import Optional
from maze import create_maze, add_horizontal_wall, add_vertical_wall
from maze import get_dimensions
from runner import create_runner, explore

def maze_reader(file_name: str):
    """
    Reads text file and turns it into a maze structure
    Checks for errors like empty files, formatting etc
    Parameter: file_name
    Returns: constructed maze 
    """
    try:
        #try to open the file in read mode
        with open(file_name, 'r') as f:
            #make a list of lines, removing empty space at ends
            lines = [line.rstrip() for line in f if line.strip()]
    except IOError:
        #end if file can't be opened
        raise IOError(f"Unable to read file: {file_name}")

    if not lines:
        #end if the file has no lines/text
        raise ValueError("File is empty")

    coord_line_index = -1
    #look backwards from the end of the file to find numbers
    for i in range(len(lines) - 1, -1, -1):
        #check if the line only has digits and spaces
        if all(c.isdigit() or c.isspace() for c in lines[i]):
            coord_line_index = i
            break
            #when the coordinates are found end the search

    if coord_line_index == -1:
        #if there was no coordinate line, raise an error
        raise ValueError("Missing coordinate line")

    #get the line with the dimensions
    coord_line = lines[coord_line_index]

    #the maze drawing is everything before the numbers
    maze_lines = lines[:coord_line_index]

    if not maze_lines:
        #error if there is no drawing
        raise ValueError("No maze structure found")

    #remove the very last line of the drawing part
    maze_lines = lines[:-1]
    if not maze_lines:
        raise ValueError("No maze structure found")

    #calculate height based on number of text lines
    height = (len(maze_lines) - 1) // 2
    #calculate width based on the numbers in the coord line
    width = len(coord_line.split())

    if width <= 0 or height <= 0:
        raise ValueError("Invalid dimensions")

    #make the empty maze first
    maze = create_maze(width, height)

    #loop to find horizontal walls
    for i in range(2, len(maze_lines), 2):
        y = height - (i // 2)
        line = maze_lines[i]
        for x in range(width):
            idx = 1 + (x * 2)
            #check if there is a hash symbol
            if idx < len(line) and line[idx] == '#':
                add_horizontal_wall(maze, x, y)

    #loop to find vertical walls
    for i in range(1, len(maze_lines), 2):
        y = height - 1 - ((i - 1) // 2)
        line = maze_lines[i]
        for x in range(1, width):
            idx = x * 2
            #check if there is a hash symbol
            if idx < len(line) and line[idx] == '#':
                add_vertical_wall(maze, y, x)

    return maze

def shortest_path(maze: list[any], starting: Optional[tuple[int, int]] = None, \
                  goal: Optional[tuple[int, int]] = None):
    """
    Finds one of the shortest paths from starting and goal
    Uses the explore function then removes any loops
    Parameters: maze, starting and goal
    Returns: a cleaned path list and the full moves list
    """
    width, height = get_dimensions(maze)

    #check if start is None, default to (0,0)
    if starting is None:
        start_x, start_y = 0, 0
    else:
        start_x, start_y = starting

    #check if goal is None, default to top right
    if goal is None:
        goal_x, goal_y = width - 1, height - 1
    else:
        goal_x, goal_y = goal

    #make the runner, and allow the runner to explore the maze
    runner = create_runner(start_x, start_y)
    full_moves = explore(runner, maze,(goal_x, goal_y))
    path = []
    repeated = {}

    #look through every move
    for x, y, action in full_moves:
        #if the same area is repeated twice, it means the runner looped
        if (x, y) in repeated:
            #find the first time the runner passed the repeated area
            idx = repeated[(x, y)]
            #cut the path back to that area
            path = path[:idx]
            #restart the repeated list for the shorter path
            repeated = {pos: i for i, (pos, _) in enumerate(path)}

        #add the current move to the path
        path.append(((x, y), action))
        #remember the repeated area
        repeated[(x, y)] = len(path) - 1

    #clean up the list format for the return
    cleaned_path = [(x, y, action) for ((x, y), action) in path]

    return cleaned_path, full_moves

if __name__ == "__main__":
    #set up the argument parser to read command line inputs
    parser = argparse.ArgumentParser(description="ECS Maze Runner")
    #add arguments for file name, start and goal
    parser.add_argument("maze", help="The name of the maze file")
    parser.add_argument("--starting", help="Start pos, e.g., '2, 1'")
    parser.add_argument("--goal", help="Goal pos, e.g., '4, 5'")

    args = parser.parse_args()

    try:
        #try to build the maze from the file
        maze = maze_reader(args.maze)
        width, height = get_dimensions(maze)

        start_pos = None
        #check if the user gave a starting position
        if args.starting:
            try:
                #split the string "x,y" into numbers
                parts = args.starting.split(',')
                sx = int(parts[0].strip())
                sy = int(parts[1].strip())
                #make sure start is inside the maze
                if not (0 <= sx < width and 0 <= sy < height):
                    raise ValueError("Starting position out of bounds")
                start_pos = (sx, sy)
            except (ValueError, IndexError):
                print("Error: Invalid starting position")
                sys.exit(1)

        goal_pos = None
        #check if the user gave a goal position
        if args.goal:
            try:
                #split the string x,y into numbers
                parts = args.goal.split(',')
                gx = int(parts[0].strip())
                gy = int(parts[1].strip())
                #check if goal is inside maze
                if not (0 <= gx < width and 0 <= gy < height):
                    raise ValueError("Goal position out of bounds")
                goal_pos = (gx, gy)
            except (ValueError, IndexError):
                print("Error: Invalid goal position")
                sys.exit(1)

        #find the shortest path
        cleanpath, moves = shortest_path(maze, start_pos, goal_pos)

        #print the cleaned path to the console
        print(cleanpath)

        #write the full exploration history to a CSV file
        with open("exploration.csv", "w") as f:
            f.write("Step,x-coordinate,y-coordinate,Actions\n")
            #loop through moves and number them
            for i, (x, y, action) in enumerate(moves, 1):
                f.write(f"{i},{x},{y},{action}\n")

        #calculate the score
        exploration_steps = len(moves)
        path_length = len(cleanpath)
        score = (exploration_steps / 4) + path_length

        #get coordinates for the stats file
        path_coords = [(x, y) for x, y, action in cleanpath]

        #write the statistics to a text file
        with open("statistics.txt", "w") as f:
            f.write(f"{args.maze}\n")
            f.write(f"{score}\n")
            f.write(f"{exploration_steps}\n")
            f.write(f"{path_coords}\n")
            f.write(f"{path_length}\n")

    except (IOError, ValueError) as e:
        #catch known errors and print the errors
        print(f"Error: {e}")
        sys.exit(1)
    except Exception as e:
        #catch any other errors that are unexpected
        print(f"Unexpected error: {e}")
        sys.exit(1)