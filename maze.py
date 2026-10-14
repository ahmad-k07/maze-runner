def create_maze(width: int = 5, height: int = 5):
    """
    Creates a maze with a specific width and height
    The default size is a 5x5 maze
    It makes the external walls but doesn't make internal walls
    Parameters: width and height (integers)
    Returns: the newly created maze as a list
    """
    #start with an empty list to hold rows (which is the height)
    maze = []
    #loop through the height to make rows as rows = height
    for y in range(height):
        row = []
        #loop through width to make the cells in the row (width = columns)
        for x in range(width):
            #create a dictionary for walls
            #checks if on the edge to set walls to True
            cell = {
                "N": (y == height - 1),  #top edge has a north wall
                "E": (x == width - 1),  #right edge has east wall
                "S": (y == 0),  #bottom edge has south wall
                "W": (x == 0),  #left edge has west wall
            }
            row.append(cell)
            #put the cell into the current row

        maze.append(row)
        #add the finished row to the maze list
        #keeps looping and adding rows until it reaches height value
    return maze

def add_horizontal_wall(maze: list[any], x_coordinate: int, horizontal_line: int):
    """
    Adds a horizontal wall inside the maze at a specific point
    Updates the cell above and below the line to where the wall is added
    Parameters: the maze, x coordinate, and horizontal line
    Returns: maze with the new wall added
    """
    #check if the horizontal line is inside the maze bounds
    if 0 <= horizontal_line < len(maze):
        #set the south wall of the cell above the line
        maze[horizontal_line][x_coordinate]["S"] = True

    #check if the row below exists
    if horizontal_line - 1 >= 0:
        #set the north wall of the cell below the line
        maze[horizontal_line - 1][x_coordinate]["N"] = True

    return maze

def add_vertical_wall(maze: list[any], y_coordinate: int, vertical_line: int):
    """
    Adds a vertical wall inside the maze at a certain area
    Updates the cell to the left and to the right
    Parameters: the maze, y coordinate, and the vertical line
    Returns: maze with the new wall added
    """
    y = y_coordinate
    x = vertical_line

    #check if the vertical line is inside the maze bounds
    if 0 <= vertical_line < len(maze[0]):
        #set the west wall of the cell to the right
        maze[y_coordinate][vertical_line]["W"] = True

    # check if the column to the left exists
    if vertical_line - 1 >= 0:
        #set the east wall of the cell to the left
        maze[y_coordinate][vertical_line - 1]["E"] = True

    return maze

def get_dimensions(maze: list[any]) -> tuple[int, int]:
    """
    Finds out how big the maze is
    It counts the rows (height) and columns (width) in the list
    Parameter: maze
    Returns: a tuple, (width, height)
    """
    rows = len(maze)
    #if the maze is empty return 0 size
    if rows == 0:
        return (0, 0)

    #width can be found by finding the length of just one row
    columns = len(maze[0])
    return (columns, rows)

def get_walls(maze: list[any], x_coordinate: int, y_coordinate: int) \
        -> tuple[bool, bool, bool, bool]:
    """
    Checks where the walls are for a specific cell
    By looking at the dictionary inside the maze list
    Parameters: maze, x and y coordinates
    Returns: tuple of booleans (north, east, south, west)
    """
    #get the specific cell dictionary using x and y coordinates
    cell = maze[y_coordinate][x_coordinate]

    #return the values for each direction
    return (cell["N"], cell["E"], cell["S"], cell["W"])