#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Artificial agent """

# ---- Imports ----
import numpy as np

from virtual_room import Room_Agent, Mutative_Agent


# ---- Class ----
class Artificial_Agent(Room_Agent, Mutative_Agent):
    """ Artificial agent with mutative neural network"""

    def __init__(self, own_map=None, initial_position=None, initial_direction=90, network=None,
                 weights_file='mutative.h5'):
        Room_Agent.__init__(self, own_map, initial_position, initial_direction)
        Mutative_Agent.__init__(network, weights_file)

    def choose_direction(self):
        # self.scan_map(self.map, self.position[0], self.position[1], self.direction)
        datas = self.data_on_front()
        predictions = self.net.predict(np.array([datas]))
        return predictions[0]

    def execute_actions(self):
        actions = {
            0: [self.rotate, (self.direction + 270)],  # tourne à droite
            1: [self.rotate, (self.direction + 90)],  # tourne à gauche
            2: [self.move, (self.position[0] + int(np.round(np.cos(np.deg2rad(self.direction)))),  # avance tout droit
                            self.position[1] + int(np.round(np.sin(np.deg2rad(self.direction)))))]
        }
        predictions = self.choose_direction()
        better = max(predictions)
        better_index = predictions.index(better)
        action = actions.get(better_index)
        if better_index < 2:  # rotation
            result = action[0](action[1][0])
        else:  # move
            result = action[0](action[1][0], action[1][1])
