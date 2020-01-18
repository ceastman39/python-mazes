class MazeNode:
    def __init__(self, default_node_value = None, set = None):
        self._top_node    = default_node_value
        self._bottom_node = default_node_value
        self._left_node   = default_node_value
        self._right_node  = default_node_value
        self._node_set    = set
        self._NODE_STATE  = None

    @property
    def node_set(self):
        return self._node_set

    @node_set.setter
    def node_set(self, value):
        self._node_set = value

    @property
    def top_node(self):
        return self._top_node

    @top_node.setter
    def top_node(self, value):
        self._top_node = value

    @property
    def bottom_node(self):
        return self._bottom_node

    @bottom_node.setter
    def bottom_node(self, value):
        self._bottom_node = value

    @property
    def left_node(self):
        return self._left_node

    @left_node.setter
    def left_node(self, value):
        self._left_node = value

    @property
    def right_node(self):
        return self._right_node

    @right_node.setter
    def right_node(self, value):
        self._right_node = value
