import math
import random
from itertools import product
from time import sleep

import numpy as np
import sys
import logging

import qi

COST_OF_SINGLE_MOVE = 10

POOLING_FACTOR = 5

IS_FINISHED = False


def start_exploration_search(exploration, radius):
    while not IS_FINISHED:
        exploration.explore(radius)


def start_random_search(exploration, motion):
    while not IS_FINISHED:
        random_x = random.uniform(2, 3) * random.choice((-1, 1))
        random_y = random.uniform(2, 3) * random.choice((-1, 1))

        target = [random_x, random_y, 0.]
        logging.info('move to ' + str(target))
        logging.info('currently at ' + str(exploration.get_current_position()))
        sleep(3)
        exploration.navigate_to(random_x, random_y, 0)

def start_search(exploration, map_exploration):
    # map = exploration_map.get_current_map()  # 0 = obstacle / 50 = not explored / 100 = free
    map_obstacles = (-1 * (100 - map_exploration)) * 2  # 0 = free / -100 = not explored / -200 = obstacle
    map_movement = np.zeros_like(map_obstacles)

    movement_future = None
    exploration.relocate_in_map([0, 0, 0])

    while not IS_FINISHED:
        position = exploration.get_current_position_in_map_array()
        current_x = position[0]
        current_y = position[1]

        pooled_shape = np.divide(map_movement.shape, POOLING_FACTOR)
        map_movement_pooled = np.zeros(pooled_shape)

        target_position = None
        while target_position is None:
            target_position = do_multiple_virtual_moves(
                current_x,
                current_y,
                map_movement_pooled,
                map_obstacles,
                2)

        position = exploration.get_current_position_in_map_array()
        x_diff = target_position[0] - position[0]
        y_diff = target_position[1] - position[1]

        target_angle = math.atan(x_diff / y_diff+1e-10)

        if x_diff < 0 and y_diff < 0:
            target_angle = math.pi - target_angle
        if x_diff > 0 and y_diff < 0:
            target_angle = -(math.pi - target_angle)
        # exploration.move_to_in_map([current_x, current_y])
        meters_per_pixel = exploration.get_meters_per_pixel()

        if movement_future is not None:
            movement_future.wait()

        logging.info('movement offset x=' + str(x_diff) + ' y=' + str(y_diff) + ' theta=' + str(target_angle))
        logging.info('')
        sleep(1)
        print "Sleep"
        movement_future = qi.async(exploration.navigate_to,
                                   math.fabs(x_diff * meters_per_pixel),
                                   math.fabs(y_diff * meters_per_pixel),
                                   -position[2] + target_angle, delay=0)

        # array_to_bw_bitmap(map_obstacles, 'c:/tmp/roblab/map-obstacles.bmp')
        # array_to_bw_bitmap(map_movement_pooled, 'c:/tmp/roblab/pooled-map.bmp')


def do_multiple_virtual_moves(current_x, current_y, map_movement, map_obstacles, max_step_number):
    step_number = 0
    current_x_pooled = current_x / POOLING_FACTOR
    current_y_pooled = current_y / POOLING_FACTOR

    while step_number < max_step_number:
        map_movement[current_y_pooled][current_x_pooled] = map_movement[current_y_pooled][current_x_pooled] - COST_OF_SINGLE_MOVE

        # map_learn_distributed = scipy.ndimage.filters.gaussian_filter(map_learn, sigma=30)

        new_x, new_y = find_next_move(map_movement, current_x_pooled, current_y_pooled)

        current_x_pooled = new_x
        current_y_pooled = new_y
        logging.info('step ' + str(step_number))
        logging.info('moved to (' + str(current_x) + '|' + str(current_y) + ')')
        step_number = step_number + 1

    target_position = find_free_field_in_subarray(current_x_pooled, current_y_pooled, map_obstacles)

    return target_position


def find_free_field_in_subarray(current_x, current_y, map_obstacles):
    for x in range(current_x*POOLING_FACTOR, (current_x + 1) * POOLING_FACTOR):
        for y in range(current_y*POOLING_FACTOR, (current_y + 1) * POOLING_FACTOR):
            if map_obstacles[x, y] == 0:
                return (x, y)

    return None


def find_next_move(map_movement, current_x, current_y):
    max_neighbour = get_max_neighbour(current_y, current_x, map_movement)

    logging.info('found max neighbour at ' + str(max_neighbour))

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
