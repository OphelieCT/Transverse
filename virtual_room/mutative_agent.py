#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" An agent with neural network wich can mutate """

import copy

# ---- Imports ----
import numpy as np
from keras import models, layers

# ---- Settings ----
np.random.seed()


# ---- Class ----
class Mutative_Agent:
    """ An agent with neural network wich can mutate """

    def __init__(self, mutation_rate=0.3, network=None, weights_file='mutative.h5'):
        self.score = 0
        self.weights_file = weights_file
        self.mutation_rate = mutation_rate
        self.net = network
        if self.net is None:
            self.net = self.build_net()

    def __lt__(self, other):
        return self.score < other.score

    @staticmethod
    def build_net():
        """ Inputs are :
         If obstacle on front
         If unknown area on front
         Amount of greatest reward on front

         Outputs are :
         Turn on left
         Turn on right
         Go forward"""
        model = models.Sequential([
            layers.Dense(9, input_dim=3, activation='relu'),
            layers.Dropout(0.1),
            layers.Dense(54, activation='relu'),
            layers.Dropout(0.1),
            layers.Dense(3, activation='softmax')
        ])
        model.compile(optimizer='adadelta', loss='binary_crossentropy', metrics=['accuracy'])
        return model

    def try_to_mutate(self):
        if np.random.randint(0, 101) < self.mutation_rate:
            self.mutation()

    def mutation(self):
        """ Create second neural network and mix both with 1/10 variation """
        temp = [self.net] * 9 + [self.build_net()]
        self.net = self.cross(temp)

    @staticmethod
    def cross(networks):
        """ Mix each network in list with the first layer by layer """
        if type(networks) not in (tuple, list, np.ndarray):
            return None
        try:
            temp_net = networks[0]
            for i in range(1, len(networks)):
                for j in range(len(temp_net.layers)):
                    temp_weights = temp_net.layers[j].get_weights()
                    input_weights = networks[i].layers[j].get_weights()
                    for _ in range(len(temp_weights)):
                        if np.random.randint(0, 101) < 50:
                            temp_weights[_] = input_weights[_]
                        # temp_weights[_] += input_weights[_]
                        # temp_weights[_] /= len(networks)
                    temp_net.layers[j].set_weights(temp_weights)
        except ValueError:
            return None
        return temp_net

    @staticmethod
    def evolve_population(population, winner_percentage=0.3, other_percentage=0.3, new_population_length=None):
        if new_population_length is None:
            new_population_length = len(population)
        population = sorted(population)
        if population[0].score < population[-1].score:  # DEBUG
            print('[DEBUG] ERROR')
            exit(0)
        winner_index = (int(len(population)) * winner_percentage) + 1
        winners = population[:winner_index]
        population = population[winner_index:]
        losers_size = int(len(population) * other_percentage)
        for i in range(losers_size):
            new_survivor_index = np.random.randint(0, len(population))
            winners.append(population[new_survivor_index])
            population.pop(new_survivor_index)
        winners = (np.random.shuffle(np.array(winners))).tolist()
        new_population = []
        # mix_list = []
        for i in range(new_population_length):
            first = 0
            second = 0
            while first == second:  # and ((first, second) in mix_list or (second, first) in mix_list):
                first = np.random.randint(0, len(winners))
                second = np.random.randint(0, len(winners))
            # mix_list.append((first, second))
            # mix_list.append((second, first))
            mixing = [copy.copy(winners[first]), copy.copy(winners[second])]
            new_population.append(Mutative_Agent.cross(mixing))
        for net in new_population:
            net.try_to_mutate()
        return new_population
