import png, os, copy
from mazegen import Maze, MazeVisualizer, MazeNode
from random import randint, sample
from math import ceil

# =====================================================================
# || MazeGenerator.py:
# ||  Used to create a solveable maze, with the option to export as raw
# ||  data or as an image file.
# =====================================================================
class MazeGenerator:
    def __init__(self):
        self._maze_visualizer = MazeVisualizer.MazeVisualizer(framerate = 45,
                                                              upscale_factor = 10)
        self._maze = None

    @property
    def maze(self):
        return self._maze

    def __create_maze_ellers(self, width, height, h_bias = 0.5, v_bias = 0.5):
        set_num = 1
        self._maze[0][0].node_set = set_num
        #Assign node sets, give connections/walls
        set_start = 0
        for x in range(self._maze.width):
            if(randint(0, 100) < 25):
                #Remove walls
                if(x+1 < self._maze.width):
                    self._maze[0][x].right_node = self._maze[0][x+1]
                    self._maze[0][x+1].left_node = self._maze[0][x]
                    self._maze[0][x+1].node_set = self._maze[0][x].node_set
            else:
                set_num += 1
                if(x+1 < self._maze.width):
                    self._maze[0][x+1].node_set = set_num
                #Remove floors
                floors_min = 1
                floors_max = int(ceil((x-set_start+1) * v_bias))
                add_floor = sample(range(set_start, x+1), randint(floors_min, floors_max))
                for index in add_floor:
                    self._maze[0][index].bottom_node = self._maze[1][index]
                    self._maze[1][index].top_node = self._maze[0][index].bottom_node
                    self._maze[1][index].node_set = self._maze[0][index].node_set
                set_start = x + 1
                if(self._maze_visualizer.IS_RECORDING):
                    self._maze_visualizer.generate_frame(self._maze)

        for y in range(1, self._maze.height):
            for x in range(self._maze.width):
                #Remove all connections
                self._maze[y][x].right_node = None
                if(x+1 < self._maze.width):
                    self._maze[y][x+1].left_node = None
                #Remove cells with bottom walls from their set.
                if(self._maze[y][x].bottom_node):
                    self._maze[y][x].top_node = self._maze[y-1][x]
                    self._maze[y-1][x].bottom_node = self._maze[y][x]
                    self._maze[y][x].node_set = self._maze[y-1][x].node_set
                else:
                    set_num += 1
                    self._maze[y][x].node_set = set_num
            set_start = 0

            for x in range(self._maze.width):
                if(x+1 < self._maze.width and self._maze[y][x].node_set == self._maze[y][x+1].node_set):
                    self._maze[y][x].right_node = None
                    self._maze[y][x+1].left_node = None
                else:
                    if(randint(0, 100) < 25 and x+1 < self._maze.width):
                        self._maze[y][x].right_node = self._maze[y][x+1]
                        self._maze[y][x+1].left_node = self._maze[y][x]
                        self._maze[y][x+1].node_set = self._maze[y][x].node_set
                    else:
                        floors_min = 1
                        floors_max =int(ceil((x-set_start+1) * v_bias))
                        add_floor = sample(range(set_start, x+1), floors_max)
                        if(y+1 < self._maze.height):
                            for index in add_floor:
                                self._maze[y][index].bottom_node = self._maze[y+1][index]
                                self._maze[y+1][index].top_node = self._maze[y][index].bottom_node
                        set_start = x + 1
                if(self._maze_visualizer.IS_RECORDING):
                    self._maze_visualizer.generate_frame(self._maze)
        #Finish the bottom row
        for x in range(self._maze.width):
            y = self._maze.height-1
            if(x+1 < self._maze.width):
                if(self._maze[y][x].node_set != self._maze[y][x+1].node_set):
                    self._maze[y][x].right_node = self._maze[y][x+1]
                    self._maze[y][x+1].left_node = self._maze[y][x]
            if(self._maze_visualizer.IS_RECORDING):
                self._maze_visualizer.generate_frame(self._maze)


    # ========================================
    # || generate:
    # ||  Generate a maze. Write more later :-)
    # ========================================
    def generate(self, height, width, record_vid = False):
        self._maze = Maze.Maze(width, height)
        if(record_vid):
            self._maze_visualizer.start_recording()
        #Randomly select start cell.
        #start_cell = (randint(0, height), randint(0, width))
        #Initiate maze creation.
        #self.__create_maze(start_cell)
        #self._maze[start_cell[0]][start_cell[1]] = self._maze.CELL_START

        self.__create_maze_ellers(width, height)
        if(record_vid):
            self._maze_visualizer.generate_frame(self._maze)
            self._maze_visualizer.stop_recording()

        self._maze_visualizer.generate_snapshot(self._maze)
        return
