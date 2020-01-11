#pypng
import png, os
from shutil import rmtree
from random import randint, sample
'''
=====================================================================
|| MazeGen.py:
||  Used to create a solveable maze, with the option to export as raw
||  data or as an image file.
=====================================================================
'''
class mazegen:
    def __init__(self):
        self._black = (0, 0, 0)
        self._white = (255, 255, 255)
        self._red   = (255, 0, 0)
        self._green = (0, 255, 0)
        self._blue  = (0, 0, 255)

        self._CELL_WALL     = 0
        self._CELL_PATH     = 1
        self._CELL_START    = 2
        self._CELL_END      = 3

        self._TOP       = 0
        self._BOTTOM    = 1
        self._LEFT      = 2
        self._RIGHT     = 3

        self._GENERATE_VID      = False
        self._FRAME_DIRECTORY   = ".\\temp_dir"
        self._FRAME_PATH        = self._FRAME_DIRECTORY + "\\img_"
        self._FRAME_FILE_TYPE   = ".png"
        self._frame = 0

        self._maze = []

    #Color Getters
    @property
    def black(self):
        return self._black

    @property
    def white(self):
        return self._white

    @property
    def red(self):
        return self._red

    @property
    def green(self):
        return self._green

    @property
    def blue(self):
        return self._blue

    '''
    ================================================
    || __create_maze:
    ||  Generate a 2D Integer Array containing data
    ||  for a solveable maze.
    ||=====
    ||  0 -> Wall/Black Cell
    ||  1 -> Path/White Cell
    ||  2 -> Start/Green Cell
    ||  3 -> End/Red Cell
    ================================================
    '''
    def __create_maze(self, cell):
        self._maze[cell[0]][cell[1]] = self._CELL_PATH
        if(self._GENERATE_VID):
            frame_name = f"{self._FRAME_PATH}{self._frame}{self._FRAME_FILE_TYPE}"
            self._frame += 1
            self.__output_png(frame_name)

        #Randomize check order.
        func_list = sample([self.__check_top, self.__check_bottom, self.__check_left, self.__check_right], 4)

        for func in func_list:
            ret_val = func(cell)
            if(ret_val[0] != -1):
                self.__create_maze(ret_val)
        return

    def __check_top(self, cell):
        check_cell = (cell[0] - 1, cell[1])
        if(check_cell[0] >= 0):
            if(self.__check_valid(check_cell)):
                return check_cell
        return (-1, -1)

        return "top";

    def __check_bottom(self, cell):
        check_cell = (cell[0] + 1, cell[1])
        if(check_cell[0] < len(self._maze)):
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
        if(check_cell[1] < len(self._maze)):
            if(self.__check_valid(check_cell)):
                return check_cell
        return (-1, -1)

    def __check_valid(self, cell):
        num_adjacent_walls = 0
        #Top
        if(cell[0] - 1 < 0 or self._maze[cell[0] - 1][cell[1]] == self._CELL_WALL):
            num_adjacent_walls += 1

        #Bottom
        if(cell[0] + 1 >= len(self._maze) or self._maze[cell[0] + 1][cell[1]] == self._CELL_WALL):
            num_adjacent_walls += 1

        #Left
        if(cell[1] - 1 < 0 or self._maze[cell[0]][cell[1] - 1] == self._CELL_WALL):
            num_adjacent_walls += 1

        #Right
        if(cell[1] + 1 >= len(self._maze) or self._maze[cell[0]][cell[1] + 1] == self._CELL_WALL):
            num_adjacent_walls += 1

        if(num_adjacent_walls >= 3):
            return True

        return False


    def __output_png(self, name):
        size = len(self._maze)
        img = []
        for y in range(0, size):
            row = ()
            for x in range(0, size):
                val = 0
                if(self._maze[y][x] == self._CELL_WALL):
                    val = self.black
                elif(self._maze[y][x] == self._CELL_PATH):
                    val = self.white
                elif(self._maze[y][x] == self._CELL_START):
                    val = self.green
                #Should be the end cell. self._CELL_END
                else:
                    val = self.red
                row = row + val
            img.append(row)
        with open(name, 'wb') as f:
            w = png.Writer(size, size, greyscale=False)
            w.write(f, img)
        return


    '''
    ========================================
    || generate:
    ||  Generate a maze. Write more later :-)
    ========================================
    '''
    def generate(self, dim, gen_vid = False):
        self._GENERATE_VID = gen_vid
        if(gen_vid):
            try:
                os.mkdir(self._FRAME_DIRECTORY)
            except OSError as err:
                print(f"Unable to create directory {self._FRAME_DIRECTORY}: {err}")
            else:
                print("Directory created...")
        #Create the 2D Maze Array
        self._maze = [[self._CELL_WALL for i in range(dim)] for j in range(dim)]
        #Randomly select start cell.
        start_cell = (randint(1, dim-1), randint(1, dim-1))
        #Initiate maze creation.
        self.__create_maze(start_cell)
        self._maze[start_cell[0]][start_cell[1]] = self._CELL_START

        if(self._GENERATE_VID):
            frame_name = f"{self._FRAME_PATH}{self._frame}{self._FRAME_FILE_TYPE}"
            self._frame += 1
            self.__output_png(frame_name)

            try:
                os.system('ffmpeg -r 30 -i "./temp_dir/img_%d.png" -vcodec mpeg4 -y "gen.mp4"')
            except OSError as err:
                print(f"Unable to generate mp4: {err}")
            else:
                print("MP4 Generated.")

            try:
                rmtree(self._FRAME_DIRECTORY)
            except OSError as err:
                print(f"Unable to remove directory {self._FRAME_DIRECTORY}: {err}")
            else:
                print("Directory removed.")

        self.__output_png("maze.png")
        return
