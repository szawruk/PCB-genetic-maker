from enum import Enum


class Direction(Enum):
    NORTH = 1
    EAST = 2
    SOUTH = -1
    WEST = -2
    dir_list = [-2, -1, 1, 2]
