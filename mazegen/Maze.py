class Maze:
    def __init__(self, height, width):
        self._CELL_WALL     = 0
        self._CELL_PATH     = 1
        self._CELL_START    = 2
        self._CELL_END      = 3

        self._height    = height
        self._width     = width

        self._data = [[self._CELL_WALL for i in range(height)] for j in range(width)]


    def __getitem__(self, index):
        return self._data[index]

    def __setitem__(self, index, value):
        this._data[index] = value

    # ====================
    # START GETTERS/SETTER
    # ====================
    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data

    @property
    def CELL_WALL(self):
        return self._CELL_WALL

    @CELL_WALL.setter
    def CELL_WALL(self, value):
        raise AttributeError("Cannot change the value of CELL_WALL")

    @property
    def CELL_PATH(self):
        return self._CELL_PATH

    @CELL_PATH.setter
    def CELL_PATH(self, value):
        raise AttributeError("Cannot change the value of CELL_PATH")

    @property
    def CELL_START(self):
        return self._CELL_START

    @CELL_START.setter
    def CELL_START(self, value):
        raise AttributeError("Cannot change the value of CELL_START")

    @property
    def CELL_END(self):
        return self._CELL_END

    @CELL_END.setter
    def CELL_END(self, value):
        raise AttributeError("Cannot change the value of CELL_END")

    @property
    def width(self):
        return self._width

    @width.setter
    def width(self, value):
        raise AttributeError("Cannot change the value of width outside of the object declaration.")

    @property
    def height(self):
        return self._height

    @height.setter
    def height(self, value):
        raise AttributeError("Cannot change the value of height outside of the object declaration.")
    # ====================
    # END GETTERS/SETTER
    # ====================
