import png, os
from mazegen import Maze
from shutil import rmtree
from random import randint, sample

# =====================================================================
# || MazeGenerator.py:
# ||  Used to create a solveable maze, with the option to export as raw
# ||  data or as an image file.
# =====================================================================
class MazeGenerator:
    def __init__(self):
        self._black = (0, 0, 0)
        self._white = (255, 255, 255)
        self._red   = (255, 0, 0)
        self._green = (0, 255, 0)
        self._blue  = (0, 0, 255)

        self._GENERATE_VID      = False
        self._FRAME_DIRECTORY   = ".\\temp_dir"
        self._FRAME_PATH        = self._FRAME_DIRECTORY + "\\img_"
        self._FRAME_FILE_TYPE   = ".png"
        self._frame = 0

        self._maze = None

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

    @property
    def maze(self):
        return self._maze

    # ================================================
    # || __create_maze:
    # ||  Generate a 2D Integer Array containing data
    # ||  for a solveable maze.
    # ================================================
    def __create_maze(self, cell):
        self._maze[cell[0]][cell[1]] = self._maze.CELL_PATH
        if(self._GENERATE_VID):
            frame_name = f"{self._FRAME_PATH}{self._frame}{self._FRAME_FILE_TYPE}"
            self._frame += 1
            self.__output_png(frame_name)

        #Randomize check order.
        func_list = sample([self.__check_top, self.__check_bottom,
                            self.__check_left, self.__check_right], 4)

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


    def __output_png(self, name):
        img = []
        print(self._maze.height, self._maze.width)
        for y in range(0, self._maze.height):
            row = ()
            for x in range(0, self._maze.width):
                val = 0
                if(self._maze[y][x] == self._maze.CELL_WALL):
                    val = self.black
                elif(self._maze[y][x] == self._maze.CELL_PATH):
                    val = self.white
                elif(self._maze[y][x] == self._maze.CELL_START):
                    val = self.green
                #Should be the end cell. self._maze.CELL_END
                else:
                    val = self.red
                row = row + val
            img.append(row)
        with open(name, 'wb') as f:
            w = png.Writer(width = self._maze.width, height = self._maze.height, greyscale = False)
            w.write(f, img)
        return



    # ========================================
    # || generate:
    # ||  Generate a maze. Write more later :-)
    # ========================================
    def generate(self, height, width, gen_vid = False):
        self._GENERATE_VID = gen_vid
        self._maze = Maze.Maze(width, height)
        if(gen_vid):
            try:
                os.mkdir(self._FRAME_DIRECTORY)
            except OSError as err:
                print(f"Unable to create directory {self._FRAME_DIRECTORY}: {err}")
            else:
                print("Directory created...")
        #Randomly select start cell.
        start_cell = (randint(0, height), randint(0, width))
        #Initiate maze creation.
        self.__create_maze(start_cell)
        self._maze[start_cell[0]][start_cell[1]] = self._maze.CELL_START

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
