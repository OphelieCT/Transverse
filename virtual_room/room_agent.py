#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" An agent wich explore the room and try to map it """

# ---- Imports ----
import numpy as np


# ---- Class ----
class Room_Agent:
    """ An agent wich explore the room and try to map it """
    general_id = 0
    OBSTACLE = -1.
    UNKNOWN = -2.
    CLEAR = 0.

    def __init__(self, own_map=None, initial_position=None, initial_direction=0):
        self.id = Room_Agent.general_id
        Room_Agent.general_id += 1
        self.position = initial_position
        self.direction = initial_direction
        if own_map is not None:
            self.map = own_map
        else:
            self.map = np.array([[0]])
        if self.position is None:
            self.position = (len(self.map) // 2, len(self.map) // 2)

    def __str__(self):
        return "Agent with id {}".format(self.id)

    def move(self, next_x, next_y):
        if (0 <= next_x < len(self.map)) and (0 <= next_y < len(self.map[next_x])):
            self.position = (next_x, next_y)
            return 0
        return 1

    def scan_map(self, to_scan, pos_x, pos_y, direction):
        """ Direction {0,1,2,3} -> {haut, droite, bas, gauche}
         Recursive function wich add new cases to self.map """
        directions_list = {
            0: [0, -1],
            1: [1, 0],
            2: [0, 1],
            3: [-1, 0],
        }
        if 0 <= pos_x < len(to_scan) and 0 <= pos_y < len(to_scan[pos_x]):
            self.map[pos_x][pos_y] = to_scan[pos_x][pos_y]
            pos_x, pos_y = [pos_x, pos_y] + directions_list.get(direction)
            self.scan_map(to_scan, pos_x, pos_y, direction)

    def data_on_front(self):
        """ Returns a list with :
        [0] - If obstacle on front
        [1] - If unknown area on front
        [2] - Amount of greatest reward on front """
        datas = [0, 0, 0]
