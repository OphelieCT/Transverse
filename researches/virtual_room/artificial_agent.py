#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Artificial agent """

# ---- Imports ----
import numpy as np

from researches.virtual_room import Room_Agent
from researches.virtual_room.q_learn_agent import Evolutive_Agent


# ---- Class ----
class Artificial_Agent(Room_Agent, Evolutive_Agent):
    """ Artificial agent with mutative neural network"""

    def __init__(self, own_map=None, initial_position=None, initial_direction=90, network=None,
                 weights_file='learn.h5'):
        Room_Agent.__init__(self, own_map=own_map, initial_position=initial_position,
                            initial_direction=initial_direction)
        Evolutive_Agent.__init__(self, network=network, weights_file=weights_file)
        self.known = []
        self.states_history = []
        self.rewards_history = []
        self.predictions_history = []

    def reset_movements(self):
        self.known = []
        self.states_history = []
        self.predictions_history = []
        Room_Agent.reset_movements(self)

    def choose_direction(self):
        # self.scan_map(self.map, self.position[0], self.position[1], self.direction)
        datas = self.data_on_front()
        self.states_history.append(datas)
        predictions = self.net.predict(np.array([datas]))
        return predictions[0].tolist()

    def execute_actions(self):
        rotation_range = 10
        actions = {
            0: [self.rotate, (self.direction + (360 - rotation_range))],  # tourne à droite
            1: [self.rotate, (self.direction + rotation_range)],  # tourne à gauche
            2: [self.move, (self.position[0] + int(np.round(np.cos(np.deg2rad(self.direction)))),  # avance tout droit
                            self.position[1] - int(np.round(np.sin(np.deg2rad(self.direction)))))]
        }
        predictions = self.choose_direction()
        result = 1
        better_index = 0
        reward_bonus = 0
        score_bonus = 0
        while result != 0:
            better = max(predictions)
            better_index = predictions.index(better)
            action = actions.get(better_index)
            if better_index < 2:  # rotation
                result = action[0](action[1])
                reward_bonus = 10.
            else:  # move forward
                result = action[0](action[1][0], action[1][1])
                if result == 0:
                    case_value = self.map[self.position[0]][self.position[1]]
                    if case_value == self.UNKNOWN:
                        reward_bonus = 20
                        if self.position not in self.known:
                            score_bonus = 20
                            self.known.append(self.position)
                    elif case_value == self.OBSTACLE:
                        reward_bonus = score_bonus = -50
                    else:
                        reward_bonus = case_value + 1
                        if self.position not in self.known:
                            score_bonus = case_value + 1
                            self.known.append(self.position)
            if result != 0:
                predictions[better_index] = 0.  # remove decision
        self.score += score_bonus
        predictions[better_index] = max(min(1., predictions[better_index] + (reward_bonus / 100)), 0.)
        self.predictions_history.append(predictions)

    def learn_rewards(self):
        if len(self.rewards_history) < 1 or len(self.predictions_history) < 1:
            return
        targets_batch = np.array([self.rewards_history])
        states_batch = np.array([self.predictions_history])
        self.net.fit(states_batch, targets_batch, batch_size=5, epochs=500, verbose=0)
