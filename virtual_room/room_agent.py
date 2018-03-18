#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" An agent wich explore the room and try to map it """

import matplotlib.pyplot as plt
# ---- Imports ----
import numpy as np

# ---- Settings ----
np.random.seed()


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
        self.tested = []
        if own_map is None:
            self.map = np.array([[0]])
        if self.position is None:
            self.position = (len(self.map) // 2, len(self.map) // 2)
        elif self.position == 'random':
            self.position = (np.random.randint(len(self.map)), np.random.randint(len(self.map[0])))
        if self.direction == 'random':
            self.direction = np.random.randint(360)

    def __str__(self):
        return "Agent with id {}".format(self.id)

    def reset_tests(self):
        self.tested = []

    def reset_movements(self):
        self.movement_history = {'x': [], 'y': []}

    def resume_movements(self):
        plt.scatter(self.movement_history['x'], self.movement_history['y'])
        plt.show()

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
        return 0

    def data_on_front(self):
        """ Returns a list with :
        [0] - If obstacle on front
        [1] - If unknown area on front
        [2] - Amount of greatest reward on front """
        to_count = [Room_Agent.OBSTACLE, Room_Agent.UNKNOWN]
        totals = [0, 0, 0]
        # on compte dans un angle de 20° (centre, +10° , -10°)
        angle = 20
        bisectrix = angle // 2
        right = 360 - bisectrix  # right rotation
        left = 360 + bisectrix  # left rotation
        for angle in range(right, left + 1):
            temp_direction = self.direction + angle
            temp_direction %= 360
            self.count_values(self.position[0], self.position[1], temp_direction, to_count, totals)
        return totals

    def count_values(self, pos_x, pos_y, direction, value_to_count, totals):
        """ Direction in degrees """
        next_x, next_y = self.next_coord(pos_x, pos_y, direction)
        if 0 <= next_x < len(self.map) and 0 <= next_y < len(self.map[0]):
            to_add = {
                value_to_count[0]: 0,
                value_to_count[1]: 1,
            }
            case_value = self.map[next_x][next_y]
            if case_value in to_add.keys():
                totals[to_add.get(case_value)] = 1
                return totals
            totals[2] = max(case_value, totals[2])
            return self.count_values(next_x, next_y, direction, value_to_count, totals)

    def convert_history(self):
        temp = []
        for i in range(len(self.movement_history['x'])):
            temp.append((self.movement_history['x'][i], self.movement_history['y'][i]))
        return temp

    @staticmethod
    def next_coord(pos_x, pos_y, direction, distance=1):
        """ Direction in degrees """
        direction = np.deg2rad(direction)
        x_bonus = int(min(np.round(distance * np.sin(direction)), 1))
        y_bonus = int(min(np.round(distance * np.cos(direction)), 1))
        next_x = pos_x - x_bonus
        next_y = pos_y + y_bonus
        return next_x, next_y
