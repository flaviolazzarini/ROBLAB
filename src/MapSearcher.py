import math
from itertools import product
import numpy as np
import sys

import qi
# import scipy.ndimage

COST_OF_SINGLE_MOVE = 10

IS_FINISHED = False


def start_search(exploration, map_exploration, map_learn):
    # map = exploration_map.get_current_map()  # 0 = obstacle / 50 = not explored / 100 = free
    map_obstacles = (-1 * (100 - map_exploration)) * 2  # 0 = free / -100 = not explored / -200 = obstacle
    map_movement = np.zeros_like(map_obstacles)

    movement_future = qi.async(exploration.relocate_in_map, [0, 0],delay=0)

    position = exploration.get_current_position_in_map_array()
    current_x = position[0]
    current_y = position[1]

    while not IS_FINISHED and max(map(max, map_movement + map_obstacles)) > -COST_OF_SINGLE_MOVE:
        current_x, current_y = do_multiple_virtual_moves(
            current_x,
            current_y,
            map_learn,
            map_movement,
            map_obstacles,
            15)

        position = exploration.get_current_position_in_map_array()
        x_diff = current_x - position[0]
        y_diff = current_y - position[1]

        target_angle = math.atan(x_diff / y_diff)

        if x_diff < 0 and y_diff < 0:
            target_angle = math.pi - target_angle
        if x_diff > 0 and y_diff < 0:
            target_angle = -(math.pi - target_angle)

        # exploration.move_to_in_map([current_x, current_y])
        meters_per_pixel = exploration.get_meters_per_pixel()

        if movement_future is not None:
            movement_future.wait()

        print('movement offset x=' + str(x_diff) + ' y=' + str(y_diff) + ' theta=' + str(target_angle))
        print('')

        movement_future = qi.async(exploration.navigate_to,
                                          math.fabs(x_diff * meters_per_pixel),
                                          math.fabs(y_diff * meters_per_pixel),
                                          -position[2] + target_angle, delay=0)


def do_multiple_virtual_moves(current_x, current_y, map_learn, map_movement, map_obstacles, max_step_number):
    step_number = 0
    while step_number < max_step_number:
        if map_learn[current_y][current_x] > 0:
            map_learn[current_y][current_x] = 0
        map_movement[current_y][current_x] = map_movement[current_y][current_x] - COST_OF_SINGLE_MOVE

        #map_learn_distributed = scipy.ndimage.filters.gaussian_filter(map_learn, sigma=30)
        map_learn_distributed = map_learn

        env_obstacles = neighbors_in_radius(6, current_y, current_x, map_obstacles)
        env_learn = neighbors_in_radius(6, current_y, current_x, map_learn_distributed)
        env_movement = neighbors_in_radius(6, current_y, current_x, map_movement)

        new_x, new_y = find_next_move(env_learn, env_obstacles, env_movement, 7, 7)

        current_x = current_x + (new_x - 7)
        current_y = current_y + (new_y - 7)
        print ('step ' + str(step_number))
        print ('moved to (' + str(current_x) + '|' + str(current_y) + ')')
        step_number = step_number + 1

    return current_x, current_y


def find_next_move(map_learn_distributed, map_obstacles, map_movement, current_x, current_y):
    distributed_map = map_learn_distributed + map_obstacles + map_movement
    max_neighbour = get_max_neighbour(current_y, current_x, distributed_map)

    print('found max neighbour at ' + str(max_neighbour))

    new_x = max_neighbour[1]
    new_y = max_neighbour[0]

    return new_x, new_y


def get_max_neighbour(current_y, current_x, map):
    max_neighbour = []
    # python 2: max_value = -sys.maxint - 1
    max_value = -(sys.maxsize - 1)
    for neighbor in neighbours((current_y, current_x), map.shape[0]):
        value = map[neighbor[0]][neighbor[1]]
        if value > max_value:
            max_value = value
            max_neighbour = neighbor

    return max_neighbour


def neighbours(cell, size):
    for c in product(*(range(n - 1, n + 2) for n in cell)):
        if c != cell and all(0 <= n < size for n in c):
            yield c


def neighbors_in_radius(max_radius, row_number, column_number, array):
    return np.array(
        [[array[i][j] if i >= 0 and i < len(array) and j >= 0 and j < len(array[0]) else 0
          for j in range(column_number - 1 - max_radius, column_number + max_radius)]
         for i in range(row_number - 1 - max_radius, row_number + max_radius)])


def place_hot_spot(col, row, value, array):
    array[row][col] = value
    for neighbor in neighbors_in_radius(1, row, col, array.shape[0]):
        array[neighbor[0]][neighbor[1]] = value / 2


def clear_hot_spot(col, row, array):
    array[row][col] = 0
    for neighbor in neighbors_in_radius(1, row, col, array.shape[0]):
        array[neighbor[0]][neighbor[1]] = 0
