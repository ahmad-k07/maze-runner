# ECS Maze Runner

A maze-solving program in Python, inspired by the Micromouse competition. Written for the
Programming I module (COMP1312) at the University of Southampton, December 2025.

A runner starts somewhere in a maze it knows nothing about, explores it one cell at a time, and
works out the shortest route to the goal.

## How it works

- **`maze.py`** builds the maze as a grid of cells, each recording which of its four sides has a wall.
- **`runner.py`** models the runner (position and orientation) and explores the maze with
  **Trémaux's algorithm**: it counts how often it has visited each cell and prefers the least-visited
  way forward, so it never gets stuck in a loop.
- **`maze_runner.py`** reads a maze from a text file, validates it, runs the exploration and then
  cuts every loop out of the explored route to leave the shortest path.

## Usage

```bash
python maze_runner.py <maze file> [--starting "x, y"] [--goal "x, y"]
```

The start defaults to the bottom-left cell and the goal to the top-right cell.

It prints the shortest path and writes two files:

- `exploration.csv`: every step of the exploration (step, x, y, action)
- `statistics.txt`: the maze name, score, number of exploration steps, the path and its length

Invalid input (missing file, empty file, bad coordinates, positions outside the maze) is reported
with a clear error message instead of a crash.
