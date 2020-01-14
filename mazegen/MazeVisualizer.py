import png
from os import mkdir, path, system
from mazegen import Maze
from shutil import rmtree

class MazeVisualizer:

    def __init__(self, tmp_frame_dir = ".\\tmp_frame_dir\\",
                 framerate = 30, mp4_out_name = "gen.mp4",
                 upscale_factor = 1):
        self._BLACK   = (0, 0, 0)
        self._WHITE   = (255, 255, 255)
        self._RED     = (255, 0, 0)
        self._GREEN   = (0, 255, 0)
        self._BLUE    = (0, 0, 255)
        self._YELLOW  = (255, 255, 0)
        self._MAGENTA = (255, 0, 255)
        self._CYAN    = (0, 255, 255)

        #Video Settings
        self._UPSCALE_FACTOR = upscale_factor
        self._IS_RECORDING   = False
        self._FRAME          = 0
        self._FRAME_RATE     = framerate
        self._TEMP_FRAME_DIR = tmp_frame_dir
        self._FRAME_PREF     = "frame_"
        self._FRAME_TYPE     = ".png"
        self._FFMPEG_PATH    = f'{self._TEMP_FRAME_DIR}{self._FRAME_PREF}%d{self._FRAME_TYPE}'
        self._FFMPEG_VCODEC  = "mpeg4"
        self._VIDEO_NAME     = mp4_out_name

    # =====================
    # START GETTERS/SETTERS
    # =====================

    @property
    def BLACK(self):
        return self._BLACK

    @property
    def WHITE(self):
        return self._WHITE

    @property
    def RED(self):
        return self._RED

    @property
    def GREEN(self):
        return self._GREEN

    @property
    def BLUE(self):
        return self._BLUE

    @property
    def YELLOW(self):
        return self._YELLOW

    @property
    def MAGENTA(self):
        return self._MAGENTA

    @property
    def CYAN(self):
        return self._CYAN

    @property
    def IS_RECORDING(self):
        return self._IS_RECORDING

    # =====================
    # END GETTERS/SETTERS
    # =====================

    def generate_snapshot(self, maze, path = "maze.png"):
        img = []
        for y in range(0, maze.height):
            row = ()
            for x in range(0, maze.width):
                val = 0
                if(maze[y][x] == maze.CELL_WALL):
                    val = self.BLACK
                elif(maze[y][x] == maze.CELL_PATH):
                    val = self.WHITE
                elif(maze[y][x] == maze.CELL_START):
                    val = self.GREEN
                #Should be the end cell. maze.CELL_END
                elif(maze[y][x] == maze.CELL_PATH_STACK):
                    val = self.CYAN
                elif(maze[y][x] == maze.CELL_END):
                    val = self.RED
                else:
                    raise KeyError(f"Value '{maze[y][x]}' is not a valid cell value.")
                row = row + (val * self._UPSCALE_FACTOR)
            for i in range(self._UPSCALE_FACTOR):
                img.append(row)
        with open(path, 'wb') as f:
            w = png.Writer(width = maze.width*self._UPSCALE_FACTOR,
                           height = maze.height*self._UPSCALE_FACTOR,
                           greyscale = False)
            w.write(f, img)
        return

    def start_recording(self):
        self._IS_RECORDING = True
        self._FRAME = 0

        try:
            if(path.isdir(self._TEMP_FRAME_DIR)):
                rmtree(self._TEMP_FRAME_DIR)
            mkdir(self._TEMP_FRAME_DIR)
        except OSError as err:
            print(f"Error modifying directory: {err}")


    def stop_recording(self):
        self._IS_RECORDING = False
        self.__generate_video()

        try:
            rmtree(self._TEMP_FRAME_DIR)
        except OSError as err:
            print(f"Error removing directory: {err}")

    def generate_frame(self, maze):
        if(self._IS_RECORDING):
            path = f"{self._TEMP_FRAME_DIR}{self._FRAME_PREF}{self._FRAME}{self._FRAME_TYPE}"
            self.generate_snapshot(maze, path)
            self._FRAME += 1

    def __generate_video(self):
        system(f'ffmpeg -r {self._FRAME_RATE} -i {self._FFMPEG_PATH} -vcodec {self._FFMPEG_VCODEC} -y {self._VIDEO_NAME}')
