class Maze:
    def __init__(self, height = 10, width = 10):
        self._CELL_WALL     = 0
        self._CELL_PATH     = 1
        self._CELL_START    = 2
        self._CELL_END      = 3

        self._data = [[self._CELL_WALL for i in range(height)] for j in range(width)]

    def __getitem__(self, index):
        return this._data[index]

    def __setitem__(self, index, value):
        this._data[index] = value

    @property
    def data(self):
        return self._data

    @data.setter
    def data(self, new_data):
        self._data = new_data
