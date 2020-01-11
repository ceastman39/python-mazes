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
        self._maze_visualizer = MazeVisualizer.MazeVisualizer(framerate = 45, upscale_factor = 5)
        self._maze = None

    @property
    def maze(self):
        return self._maze

    # ================================================
    # || __create_maze:
    # ||  Generate a 2D Integer Array containing data
    # ||  for a solveable maze.
    # ================================================
    def __create_maze(self, cell):
        if(self._maze_visualizer.IS_RECORDING):
            self._maze[cell[0]][cell[1]] = self._maze.CELL_PATH_STACK
            self._maze_visualizer.generate_frame(self._maze)
        else:
            self._maze[cell[0]][cell[1]] = self._maze.CELL_PATH

        #Randomize check order.
        func_list = sample([self.__check_top, self.__check_bottom,
                            self.__check_left, self.__check_right], 4)

        for func in func_list:
            ret_val = func(cell)
            if(ret_val[0] != -1):
                self.__create_maze(ret_val)
        if(self._maze_visualizer.IS_RECORDING):
            self._maze[cell[0]][cell[1]] = self._maze.CELL_PATH
            self._maze_visualizer.generate_frame(self._maze)
        return

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
