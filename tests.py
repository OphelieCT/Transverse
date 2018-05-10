#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Main script of project """

# ---- Imports ----
import numpy as np
from matplotlib import pyplot as plt


# ---- Functions ----
def add_point(mapped, point, coord):
    relative_x = int(np.round(np.sin(np.deg2rad(point[1])) * point[0]))
    relative_y = int(np.round(np.cos(np.deg2rad(point[1])) * point[0]))

    new_x = coord[0]
    new_y = coord[1]

    point_x = new_x + relative_x
    point_y = new_y + relative_y

    if point_x >= len(mapped):
        for i in range(len(mapped), point_x + 1):
            mapped.append([0] * len(mapped[0]))
    elif point_x < 0:
        for i in range(point_x, 0):
            mapped.insert(0, [0] * len(mapped[0]))
        new_x += np.absolute(point_x)

    if point_y < 0:
        y = np.absolute(point_y)
        for i in range(len(mapped)):
            mapped[i] = [0] * y + mapped[i]
        new_y += np.absolute(point_y)
    elif point_y >= len(mapped[0]):
        length = point_y - len(mapped[0])
        for i in range(len(mapped)):
            mapped[i] += [0] * (length + 1)

    point_x = max(0, point_x)
    point_y = max(0, point_y)
    put_point(mapped, point_x, point_y, 1)
    return new_x, new_y


def put_point(mapped, x, y, code):
    mapped[x][y] = code


# ---- Script ----
if __name__ == '__main__':
    mapped = [[]]
    coord = (0, 0)
    datas = [[3 * np.sqrt(2), i] for i in range(45, 360, 90)]
    datas += [[3, i] for i in range(0, 360, 90)]
    tests = [[7, 90], [3 * np.sqrt(2), 135], [3, 180], [3 * np.sqrt(2), 225], [5, 270],
             [3 * np.sqrt(2), 315], [4, 0], [4 * np.sqrt(2), 45]]
    print("Datas : {}".format(tests))
    print("Begin :")
    print(np.array(mapped))
    for point in tests:
        coord = add_point(mapped, point, coord)

    mapped[coord[0]][coord[1]] = 5
    print("Final mapped - {}".format(coord))
    print(np.array(mapped))
    plt.imshow(np.array(mapped), interpolation='nearest')
    plt.show()
