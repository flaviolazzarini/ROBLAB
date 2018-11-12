import numpy as np
from MapHelper import array_to_bw_bitmap
from itertools import product


def neighbours(cell, size):
    for c in product(*(range(n - 1, n + 2) for n in cell)):
        if c != cell and all(0 <= n < size for n in c):
            yield c


def find_values_greater_zero(learn_layer):
    findings = []
    for row in range(learn_layer.shape[0]):
        for col in range(learn_layer.shape[1]):
            value = learn_layer[row][col]
            if value > 0:
                findings.append([value, [row, col]])

    return findings


def goto_hot_spots(exploration, learn_layer):
    findings = find_values_greater_zero(learn_layer)
    for finding in findings:
        row = finding[1][0]
        col = finding[1][1]

        # absolute variant
        exploration.move_to_in_map([col, row])

        # relative variant
        # position = exploration.get_current_pixel()
        # meters_per_pixel = exploration.get_current_map_meters_per_pixel()
        # x_offset = col - position[0]
        # y_offset = row - position[1]

        # move_x_meters = x_offset * meters_per_pixel
        # move_y_meters = y_offset * meters_per_pixel
        # exploration.navigate_to(move_x_meters, move_y_meters)


def place_hot_spot(col, row, value, array):
    array[row][col] = value
    for neighbor in neighbours((row, col), array.shape[0]):
        array[neighbor[0]][neighbor[1]] = value / 2


def clear_hot_spot(col, row, array):
    array[row][col] = 0
    for neighbor in neighbours((row, col), array.shape[0]):
        array[neighbor[0]][neighbor[1]] = 0


def start_search(exploration):
    map = exploration.get_current_map()  # 0 = obstacle / 50 = not explored / 100 = free
    map_layer = -1 * (100 - map)  # 0 = free / -50 = not explored / -100 = obstacle
    learn_layer = np.zeros_like(map_layer)
    place_hot_spot(41, 69, 255, learn_layer)

    array_to_bw_bitmap(learn_layer, "c:\\tmp\\learn_layer.bmp")

    goto_hot_spots(exploration, learn_layer)
