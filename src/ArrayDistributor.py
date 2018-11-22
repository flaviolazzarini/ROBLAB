import numpy as np


def distribute_values(array):
    array_distributed = np.copy(array)
    array = np.copy(array)
    shape = array.shape

    for y in range(shape[0]):
        for x in range(shape[1]):
            neighbors = distributed_neighbors(int((shape[0] - 1) / 1), y, x, array)
            array_distributed[y][x] = float(neighbors.sum())

    return array_distributed


def distributed_neighbors(max_radius, row_number, column_number, array):
    array_orig = np.copy(array)
    array = np.copy(array)
    x = int(column_number)
    y = int(row_number)
    column_number = column_number + 1
    row_number = row_number + 1

    distributed = np.array(
        [[get_distributed_value(i, j, max_radius, column_number, row_number, array)
          if i >= 0 and i < len(array) and j >= 0 and j < len(array[0]) else 0
          for j in range(column_number - 1 - max_radius, column_number + max_radius)]
         for i in range(row_number - 1 - max_radius, row_number + max_radius)])

    distributed[max_radius][max_radius] = array_orig[y][x]

    return distributed


def get_distributed_value(i, j, max_radius, column_number, row_number, array):
    zeroX = column_number - max_radius
    zeroY = row_number - max_radius
    current_radius = get_radius(i, j, max_radius, zeroX, zeroY)
    if current_radius != 0:
        value = array[i][j] / (current_radius ** 2)
        return value
    else:
        return array[i][j]


def get_radius(i, j, max_radius, zero_x, zero_y):
    x = abs(i - zero_x)
    y = abs(j - zero_y)
    radius = max([abs(max_radius - x), abs(max_radius - y)])
    return radius
