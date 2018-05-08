#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Main script of project """

# ---- Imports ----
from PIL import Image, ImageDraw
import numpy as np


# ---- Functions ----
def add_point(map, point, coord):
    relative_x = int(np.round(np.sin(np.deg2rad(point[1])) * point[0]))
    relative_y = int(np.round(np.cos(np.deg2rad(point[1])) * point[0]))

    new_x = coord[0]
    new_y = coord[1]

    point_x = new_x + relative_x
    point_y = new_y + relative_y

    if point_x >= len(map):
        for i in range(len(map), point_x + 1):
            map.append([0] * len(map[0]))
    elif point_x < 0:
        for i in range(point_x, 0):
            map.insert(0, [0] * len(map[0]))
        new_x += np.absolute(point_x)

    if point_y < 0:
        y = np.absolute(point_y)
        for i in range(len(map)):
            map[i] = [0] * y + map[i]
        new_y += np.absolute(point_y)
    elif point_y >= len(map[0]):
        length = point_y - len(map[0])
        for i in range(len(map)):
            map[i] += [0] * (length + 1)

    point_x = max(0, point_x)
    point_y = max(0, point_y)
    map[point_x][point_y] = 1
    return new_x, new_y


# ---- Script ----
if __name__ == '__main__':
    map = [[]]
    coord = (0, 0)
    datas = [[2 * np.sqrt(2), i] for i in range(45, 360, 90)]
    datas += [[2, i] for i in range(0, 360, 90)]
    print("Datas : {}".format(datas))
    print("Begin :")
    print(np.array(map))
    for point in datas:
        coord = add_point(map, point, coord)
        print("Step : {} - {}".format(coord, point[1]))
        print(np.array(map))
    print("Final map")
    print(np.array(map))
