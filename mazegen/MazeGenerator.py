import png, os
from mazegen import Maze, MazeVisualizer
from random import randint, sample

# =====================================================================
# || MazeGenerator.py:
# ||  Used to create a solveable maze, with the option to export as raw
# ||  data or as an image file.
# =====================================================================
class MazeGenerator:
    def __init__(self):
        self._maze_visualizer = MazeVisualizer.MazeVisualizer(framerate = 45,
                                                              upscale_factor = 8)
        self._maze = None

    @property
    def maze(self):
        return self._maze

    # ================================================
    # || __create_maze:
    # ||  Generate a 2D Integer Array containing data
    # ||  for a solveable maze. Starts off all cells
    # ||  as "walls."
    # ================================================
    def __create_maze(self, cell):
        # Capture a frame if recording a video of the generation.
        # This sets the cell to the type CELL_PATH_STACK, which is
        # the same as a normal path, except the MazeVisualizer class
        # sets the cell to a different color. It will be set back
        # to a normal path cell when popped off the stack.
        if(self._maze_visualizer.IS_RECORDING):
            self._maze[cell[0]][cell[1]] = self._maze.CELL_PATH_STACK
            self._maze_visualizer.generate_frame(self._maze)
        else:
            self._maze[cell[0]][cell[1]] = self._maze.CELL_PATH

        # Randomize the order of which adjacent cells to check.
        func_list = sample([self.__check_top, self.__check_bottom,
                            self.__check_left, self.__check_right], 4)

        # Then, execute the randomized list.
        for func in func_list:
            ret_val = func(cell)
            # If the cell given i the function is valid, push it on the stack.
            if(ret_val[0] != -1):
                self.__create_maze(ret_val)


        # Set the cell back to a normal path cell when popped off the stack.
        if(self._maze_visualizer.IS_RECORDING):
            self._maze[cell[0]][cell[1]] = self._maze.CELL_PATH
            self._maze_visualizer.generate_frame(self._maze)
        return

    # All of the following 'check' functions check the adjacent cells of
    # the given cell to see if they would be valid paths. Returns a tuple
    # of (-1, -1) if invalid, else returns the checked cell's coordinate.
    # These functions are seperated to randomize the order in which the
    # adjacent cells are checked.

    def __check_top(self, cell):
        check_cell = (cell[0] - 1, cell[1])
        if(check_cell[0] >= 0):
            if(self.__check_valid(check_cell)):
                return check_cell
        return (-1, -1)

    def __check_bottom(self, cell):
        check_cell = (cell[0] + 1, cell[1])
        if(check_cell[0] < self._maze.height):
            if(self.__check_valid(check_cell)):
                return check_cell
        return (-1, -1)

    def __check_left(self, cell):
        check_cell = (cell[0], cell[1] - 1)
        if(check_cell[1] >= 0):
            if(self.__check_valid(check_cell)):
                return check_cell
        return (-1, -1)

    def __check_right(self, cell):
        check_cell = (cell[0], cell[1] + 1)
        if(check_cell[1] < self._maze.width):
            if(self.__check_valid(check_cell)):
                return check_cell
        return (-1, -1)

    # Checks all adjacent cells to see if
    def __check_valid(self, cell):
        num_adjacent_walls = 0
        #Top
        if(cell[0] - 1 < 0 or self._maze[cell[0] - 1][cell[1]] == self._maze.CELL_WALL):
            num_adjacent_walls += 1

        #Bottom
        if(cell[0] + 1 >= self._maze.height or self._maze[cell[0] + 1][cell[1]] == self._maze.CELL_WALL):
            num_adjacent_walls += 1

        #Left
        if(cell[1] - 1 < 0 or self._maze[cell[0]][cell[1] - 1] == self._maze.CELL_WALL):
            num_adjacent_walls += 1

        #Right
        if(cell[1] + 1 >= self._maze.width or self._maze[cell[0]][cell[1] + 1] == self._maze.CELL_WALL):
            num_adjacent_walls += 1

        if(num_adjacent_walls >= 3):
            return True

        return False



    # ========================================
    # || generate:
    # ||  Generate a maze. Write more later :-)
    # ========================================
    def generate(self, height, width, record_vid = False):
        self._maze = Maze.Maze(width, height)
        if(record_vid):
            self._maze_visualizer.start_recording()
        #Randomly select start cell.
        start_cell = (randint(0, height), randint(0, width))
        #Initiate maze creation.
        self.__create_maze(start_cell)
        self._maze[start_cell[0]][start_cell[1]] = self._maze.CELL_START

        if(record_vid):
            self._maze_visualizer.generate_frame(self._maze)
            self._maze_visualizer.stop_recording()

        self._maze_visualizer.generate_snapshot(self._maze)
        return
