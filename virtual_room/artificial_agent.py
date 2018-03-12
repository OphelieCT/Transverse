#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Artificial agent """

# ---- Imports ----
import numpy as np

from virtual_room.mutative_agent import Mutative_Agent
from virtual_room.room_agent import Room_Agent


# ---- Class ----
class Artificial_Agent(Room_Agent, Mutative_Agent):
    """ Artificial agent with mutative neural network"""

    def __init__(self, own_map=None, initial_position=None, initial_direction=90, network=None,
                 weights_file='mutative.h5', mutation_rate=30):
        Room_Agent.__init__(self, own_map=own_map, initial_position=initial_position,
                            initial_direction=initial_direction)
        Mutative_Agent.__init__(self, mutation_rate=mutation_rate, network=network, weights_file=weights_file)
        self.known = []

    def choose_direction(self):
        # self.scan_map(self.map, self.position[0], self.position[1], self.direction)
        datas = self.data_on_front()
        predictions = self.net.predict(np.array([datas]))  # BUG
        return predictions[0].tolist()

    def execute_actions(self):
        actions = {
            0: [self.rotate, (self.direction + 270)],  # tourne à droite
            1: [self.rotate, (self.direction + 90)],  # tourne à gauche
            2: [self.move, (self.position[0] - int(np.round(np.cos(np.deg2rad(self.direction)))),  # avance tout droit
                            self.position[1] - int(np.round(np.sin(np.deg2rad(self.direction)))))]
        }
        predictions = self.choose_direction()
        better = max(predictions)
        better_index = predictions.index(better)
        action = actions.get(better_index)
        if better_index < 2:  # rotation
            action[0](action[1])
        else:  # move forward
            result = action[0](action[1][0], action[1][1])
            if result == 0:
                case_value = self.map[self.position[0]][self.position[1]]
                if case_value == self.UNKNOWN and self.position not in self.known:
                    self.score += 5
                    self.known.append(self.position)
                elif case_value == self.OBSTACLE:
                    self.score -= 5
                elif self.position not in self.known:
                    self.score += case_value
                    self.known.append(self.position)
