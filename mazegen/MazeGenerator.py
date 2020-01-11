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
        #Create first row, each node is it's own set.
        row = [MazeNode.MazeNode(default_node_value = False, set = i+1) for i in range(self._maze.width)]
        row[0].left_node = True

        for i in range(1, self._maze.width):

            # Randomly union together sets of cells
            if(randint(0, 1) == 1):
                row[i].node_set = row[i-1].node_set
            else:
                row[i].left_node = True
                row[i-1].right_node = True
        row[self._maze.width-1].right_node = True

        #Add bottom floor
        bottom_in_set = False
        curr_set = row[0].node_set
        for x in range(self._maze.width - 1):
            if(row[i+1])
            #=======TODO=======

        self._maze.append(row)
        self._maze.append(row)
        #Add top
        for node in self._maze[0]:
            node.top_node = True

        for y in range(1, self._maze.height):
            for node in self._maze[y]:


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
