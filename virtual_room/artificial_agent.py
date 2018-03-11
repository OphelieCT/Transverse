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

    def __init__(self, own_map=None, initial_position=None, initial_direction=0, network=None,
                 weights_file='mutative.h5'):
        Room_Agent.__init__(self, own_map, initial_position, initial_direction)
        Mutative_Agent.__init__(network, weights_file)

    def choose_direction(self):
        self.scan_map(self.map, self.position[0], self.position[1], self.direction)
        datas = self.data_on_front()
        predictions = self.net.predict(np.array([datas]))
