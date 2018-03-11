#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" An agent wich explore the room and try to map it """

import matplotlib.pyplot as plt
# ---- Imports ----
import numpy as np


# ---- Class ----
class Room_Agent:
    """ An agent wich explore the room and try to map it """
    general_id = 0
    OBSTACLE = -1.
    UNKNOWN = -2.
    CLEAR = 0.

    def __init__(self, own_map=None, initial_position=None, initial_direction=90):
        self.id = Room_Agent.general_id
        Room_Agent.general_id += 1
        self.position = initial_position
        self.direction = initial_direction  # in degrees
        self.movement_history = {'x': [], 'y': []}
        self.map = own_map
        if own_map is None:
            self.map = np.array([[0]])
        if self.position is None:
            self.position = (len(self.map) // 2, len(self.map) // 2)

    def __str__(self):
        return "Agent with id {}".format(self.id)

    def resume_movements(self):
        plt.scatter(self.movement_history['x'], self.movement_history['y'])
        return plt

    def move(self, next_x, next_y):
        if (0 <= next_x < len(self.map)) and (0 <= next_y < len(self.map[next_x])):
            self.position = (next_x, next_y)
            self.movement_history['x'].append(next_x)
            self.movement_history['y'].append(next_y)
            return 0
        return 1

    def rotate(self, to_direction):
        to_direction %= 360
        self.direction = to_direction

    def data_on_front(self):
        """ Returns a list with :
        [0] - If obstacle on front
        [1] - If unknown area on front
        [2] - Amount of greatest reward on front """
        to_count = [Room_Agent.OBSTACLE, Room_Agent.UNKNOWN]
        totals = [0, 0, 0]
        # on compte dans un angle de 20° (centre, +10° , -10°)
        angle = 20
        bisectrix = angle / 2
        datas: list = (np.array(self.count_values(self.position[0], self.position[1], np.deg2rad(self.direction),
                                                  to_count, totals)) +
                       np.array(self.count_values(self.position[0], self.position[1],
                                                  np.deg2rad((self.direction + bisectrix) % 360),
                                                  to_count,
                                                  totals)) +
                       np.array(
                           self.count_values(self.position[0], self.position[1],
                                             np.deg2rad((self.direction + 360 - bisectrix) % 360),
                                             to_count, totals))).tolist()
        for i in range(2):
            datas[i] = min(datas[i], 1)
        return datas

    def count_values(self, pos_x, pos_y, direction, value_to_count, totals):
        if self.map[pos_x][pos_y] == value_to_count[0]:
            totals[0] += 1
            return totals
        elif self.map[pos_x][pos_y] > 0:
            totals[2] += 1
            return totals
        elif self.map[pos_x][pos_y] == value_to_count[1]:
            totals[1] += 1
        next_x = pos_x - int(np.round(np.cos(direction)))
        next_y = pos_y - int(np.round(np.sin(direction)))
        if 0 <= next_x < len(self.map) and 0 <= next_y < len(self.map[0]):
            return self.count_values(next_x, next_y, direction, value_to_count, totals)
        return totals
