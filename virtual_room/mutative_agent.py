#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" An agent with neural network wich can mutate """

import copy

# ---- Imports ----
import numpy as np
from keras import models, layers
from scipy.special import comb

# ---- Settings ----
np.random.seed()


# ---- Class ----
class Mutative_Agent:
    """ An agent with neural network wich can mutate """

    def __init__(self, mutation_rate=30, network=None, weights_file='mutative.h5'):
        self.score = 0
        self.weights_file = weights_file
        self.mutation_rate = mutation_rate
        self.net = network
        if self.net is None:
            self.net = self.build_net()

    def __lt__(self, other):
        return self.score > other.score

    def save_me(self):
        try:
            self.net.save_weights(self.weights_file)
        except OSError:
            self.net.save_weights(self.weights_file[:-3] + '1' + '.h5')

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
        model.predict(np.array([[0, 0, 0]]))  # activate model
        return model

    def try_to_mutate(self):
        if np.random.randint(0, 101) < self.mutation_rate:
            self.mutation()

    def mutation(self):
        """ Create second neural network and mix both with 5% variation """
        variation = 2.5  # 5% variation
        minimal = int(100 - variation)
        maximal = int(101 + variation)
        for l in self.net.layers:
            w = l.get_weights()
            for entry in w:
                for i in range(len(entry)):
                    for j in range(len(entry[i])):
                        entry[i][j] *= np.random.randint(minimal, maximal) / 100
            l.set_weights(w)

    @staticmethod
    def cross(networks):
        """ Mix each network in list with the first layer by layer """
        if type(networks) not in (tuple, list, np.ndarray):
            return None
        try:
            temp_net = copy.copy(networks[0])  # get first network as principal and result of fusion
            for i in range(1, len(networks)):  # get each others networks
                for j in range(len(temp_net.layers)):  # work on each layer
                    temp_weights = temp_net.layers[j].get_weights()  # get weights of both net in fusion process
                    input_weights = networks[i].layers[j].get_weights()
                    for _ in range(len(temp_weights)):  # make fusion of layers
                        temp_weights[_] += input_weights[_]
                        temp_weights[_] /= len(networks)
                    temp_net.layers[j].set_weights(temp_weights)  # set new layer weights
        except ValueError:
            return None
        return temp_net

    @staticmethod
    def get_winners(population, winner_percentage=0.3):
        winner_percentage = min(1., winner_percentage)  # protection against more winners percentage than 100%
        population = sorted(population)
        winner_index = int(len(population) * winner_percentage) + 1  # to include 0 if 0 is index
        winners = population[:winner_index]
        return winners, winner_index

    @staticmethod
    def random_fusion(population, fusion_length, repetition=False):
        fusions_index = []
        fusions = []
        population_copy = []
        for obj in population:
            population_copy.append(copy.copy(obj))
        population: np.ndarray = np.array(population_copy)  # save original population and get all attributes
        np.random.shuffle(population)  # mix population
        population: list = population.tolist()
        total = comb(len(population), 2)  # maximum combinations
        while True:
            if not len(fusions) < fusion_length:
                break
            if not repetition and len(fusions) > total:
                break
            first, second = 0, 0
            while first == second and ((first, second) in fusions_index or (second, first) in fusions_index):
                first = np.random.randint(len(population))
                second = np.random.randint(len(population))
            if not repetition:  # if repetitions aren't allowed
                fusions_index.append((first, second))
                fusions_index.append((second, first))
            mixed = [population[first].net, population[second].net]  # get to mix networks
            result_net = Mutative_Agent.cross(mixed)  # make fusion
            fusions.append(
                copy.copy(population[first]))  # add new agent to new population (copy to keep its attributes and class)
            fusions[-1].net = result_net  # apply new net on new agent
        return fusions

    @staticmethod
    def copy_net(net):
        new_net = Mutative_Agent.build_net()
        for i in range(len(net.layers)):
            new_net.layers[i].set_weights(copy.deepcopy(net.layers[i].get_weights()))
        new_net.compile(optimizer='adadelta', loss='binary_crossentropy', metrics=['accuracy'])
        new_net.predict(np.array([[0, 0, 0]]))  # activate model
        return new_net

    @staticmethod
    def copy_agent(agent):
        new_agent = copy.copy(agent)
        new_agent.net = Mutative_Agent.copy_net(agent.net)
        return new_agent

    @staticmethod
    def evolve_population(population, winner_percentage=0.3, new_population_length=None):
        if new_population_length is None:
            new_population_length = len(population)
        winners, winner_index = Mutative_Agent.get_winners(population, winner_percentage)
        winners_copy = []
        for obj in winners:
            winners_copy.append(Mutative_Agent.copy_agent(obj))
        new_population = winners_copy  # winners automatically survive to the next gen
        # add fusions into new population
        fusions = Mutative_Agent.random_fusion(winners, new_population_length - len(new_population), repetition=False)
        new_population += fusions
        # make random mutations from winners and add them in new population
        for ai in winners:
            if len(new_population) < new_population_length:
                ai.try_to_mutate()
                new_population.append(ai)
            else:
                break
        # if needed, add random fusions from old population to new population
        if len(new_population) < new_population_length:
            all_fusions = Mutative_Agent.random_fusion(population, new_population_length - len(new_population),
                                                       repetition=True)
            new_population += all_fusions
        return new_population
