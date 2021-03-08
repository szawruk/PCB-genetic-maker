import random

import numpy

from Direction import Direction
from PCBData import PCBData
from Path import Path
from Segment import Segment

MAX_SEGMENTS = 20
CROSS_PENALTY_WEIGHT = 1
PATHS_LENGTH_PENALTY_WEIGHT = 2
SEGMENTS_COUNT_PENALTY_WEIGHT = 3
PATHS_NOT_IN_BOARD_PENALTY_WEIGHT = 4
SEGMENTS_OUTSIDE_BOARD_PENALTY_WEIGHT = 5


class Chromosome:
    def __init__(self, pcb_data_object: PCBData):
        self.pcb_data_object = pcb_data_object
        self.paths = []

    def generate_random_paths(self):
        # print("start generating random paths")

        for path_points in self.pcb_data_object.pcb_path_points:
            x_actual = path_points[0]
            y_actual = path_points[1]
            x_end = path_points[2]
            y_end = path_points[3]

            path = Path()

            last_used_direction = None
            path_points_connected = False
            path_segments = random.randint(2, MAX_SEGMENTS)

            while not path_points_connected:
                if path_segments > 2:
                    while True:
                        step_direction = random.sample([-2, -1, 1, 2], 1)[0]
                        if last_used_direction is None or last_used_direction != - step_direction:
                            break

                    last_used_direction = step_direction
                    step_length = random.randint(1, self.get_height_or_width_pcb(step_direction))
                    new_segment = Segment(step_direction, step_length)
                    path.segments.append(new_segment)

                    if step_direction == Direction.NORTH.value:
                        y_actual += step_length
                    if step_direction == Direction.SOUTH.value:
                        y_actual -= step_length
                    if step_direction == Direction.WEST.value:
                        x_actual -= step_length
                    if step_direction == Direction.EAST.value:
                        x_actual += step_length

                else:
                    if x_actual != x_end:
                        step_length = x_end - x_actual
                        step_direction = numpy.sign(step_length) * 2  # east and west have 2 and -2
                        x_actual += step_length
                        path.segments.append(Segment(step_direction, abs(step_length)))
                    elif y_actual != y_end:
                        step_length = y_end - y_actual
                        step_direction = numpy.sign(step_length)
                        y_actual += step_length
                        path.segments.append(Segment(step_direction, abs(step_length)))

                path_segments -= 1

                if x_actual == x_end and y_actual == y_end:
                    path_points_connected = True

            self.paths.append(path)

    def get_height_or_width_pcb(self, direction_number):
        if abs(direction_number) == 1:
            return self.pcb_data_object.pcb_height
        else:
            return self.pcb_data_object.pcb_width

    def print_me(self):

        for idx, path in enumerate(self.paths):
            x_actual = self.pcb_data_object.pcb_path_points[idx][0]
            y_actual = self.pcb_data_object.pcb_path_points[idx][1]

            print("Path " + str(idx), end='     ')
            for segment in path.segments:
                if segment.direction == Direction.WEST.value or segment.direction == Direction.EAST.value:
                    x_actual += numpy.sign(segment.direction) * segment.length
                else:
                    y_actual += numpy.sign(segment.direction) * segment.length

                print(str(x_actual) + ";" + str(y_actual), end=' ')
            print()
        print()

    def get_cross_count(self):
        pcb_height = self.pcb_data_object.pcb_height
        pcb_width = self.pcb_data_object.pcb_width

        matrix = numpy.zeros((pcb_height, pcb_width), dtype=int)

        for idx, path in enumerate(self.paths):
            x_actual = self.pcb_data_object.pcb_path_points[idx][0]
            y_actual = self.pcb_data_object.pcb_path_points[idx][1]
            matrix[x_actual][y_actual] += 1

            for segment in path.segments:
                for step in range(segment.length):
                    if segment.direction == Direction.WEST.value or segment.direction == Direction.EAST.value:
                        x_actual += numpy.sign(segment.direction)
                    else:
                        y_actual += numpy.sign(segment.direction)

                    if (x_actual in range(pcb_width)) and (y_actual in range(pcb_height)):
                        matrix[y_actual][x_actual] += 1

        # print(numpy.asmatrix(matrix))

        crosses = 0
        for x in numpy.nditer(matrix):
            if x > 1:
                crosses += sum(range(x))

        return crosses

    def get_total_path_length(self):
        total_length = 0

        for path in self.paths:
            for segment in path.segments:
                total_length += segment.length

        return total_length

    def get_total_segments_count(self):
        total_segments_count = 0

        for path in self.paths:
            total_segments_count += len(path.segments)

        return total_segments_count

    def get_paths_count_outside_board(self):
        outside_paths_count = 0

        pcb_height = self.pcb_data_object.pcb_height
        pcb_width = self.pcb_data_object.pcb_width

        for idx, path in enumerate(self.paths):
            x_actual = self.pcb_data_object.pcb_path_points[idx][0]
            y_actual = self.pcb_data_object.pcb_path_points[idx][1]

            for segment in path.segments:
                if segment.direction == Direction.WEST.value or segment.direction == Direction.EAST.value:
                    x_actual += numpy.sign(segment.direction) * segment.length
                else:
                    y_actual += numpy.sign(segment.direction) * segment.length

                if (x_actual not in range(pcb_width)) or (y_actual not in range(pcb_height)):
                    outside_paths_count += 1
                    break
        return outside_paths_count

    def get_segments_count_outside_board(self):
        length_of_paths_outside_board = 0
        pcb_height = self.pcb_data_object.pcb_height
        pcb_width = self.pcb_data_object.pcb_width

        for idx, path in enumerate(self.paths):
            x_actual = self.pcb_data_object.pcb_path_points[idx][0]
            y_actual = self.pcb_data_object.pcb_path_points[idx][1]

            for segment in path.segments:
                for step in range(segment.length):
                    if segment.direction == Direction.WEST.value or segment.direction == Direction.EAST.value:
                        x_actual += numpy.sign(segment.direction)
                    else:
                        y_actual += numpy.sign(segment.direction)

                    if (x_actual not in range(pcb_width)) or (y_actual not in range(pcb_height)):
                        length_of_paths_outside_board += 1

        return length_of_paths_outside_board

    def penalty_function(self):
        penalty_points = 0
        penalty_points += self.get_cross_count() * CROSS_PENALTY_WEIGHT\
            + self.get_total_path_length() * PATHS_LENGTH_PENALTY_WEIGHT\
            + self.get_total_segments_count() * SEGMENTS_COUNT_PENALTY_WEIGHT\
            + self.get_paths_count_outside_board() * PATHS_NOT_IN_BOARD_PENALTY_WEIGHT\
            + self.get_segments_count_outside_board() * SEGMENTS_OUTSIDE_BOARD_PENALTY_WEIGHT

        # print(f"Total line cross count: {self.get_cross_count()}")
        # print(f"Total paths length: {self.get_total_path_length()}")
        # print(f"Total segments count: {self.get_total_segments_count()}")
        # print(f"Outside paths count: {self.get_paths_count_outside_board()}")
        # print(f"Paths length outside the board: {self.get_segments_count_outside_board()}")

        return penalty_points


