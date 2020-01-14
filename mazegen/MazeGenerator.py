import png, os
from mazegen import Maze, MazeVisualizer, MazeNode
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
    #def __create_maze(self, cell):



    def __create_maze_ellers(self, width, height):
        set_num = 1
        self._maze[0][0].node_set = set_num
        #Assign node sets, give connections/walls
        set_start = 0
        for x in range(self._maze.width-1):
            if(randint(0, 1) == 1):
                #Remove walls
                self._maze[0][x].right_node = self._maze[0][x+1]
                self._maze[0][x+1].left_node = self._maze[0][x]
                self._maze[0][x+1].node_set = set_num
            else:
                set_num += 1
                self._maze[0][x+1].node_set = set_num
                #Remove floors
                add_floor = sample(range(set_start, x+1), randint(1, x-set_start+1))
                #print(f"From {set_start} to {x} => {add_floor}")
                for index in add_floor:
                    self._maze[0][index].bottom_node = self._maze[1][index]
                    self._maze[1][index].top_node = self._maze[0][index].bottom_node
                set_start = x + 1

        #======== TO DO ========




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

        #self._maze_visualizer.generate_snapshot(self._maze)
        return
