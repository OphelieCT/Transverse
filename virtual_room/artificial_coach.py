#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Class wich trains artificial agents and let them evolve """

# ---- Imports ----

import numpy as np

from virtual_room.room import Virtual_Room
from virtual_room.thread_agent import Process


# ---- Class ----
class Artificial_Coach:
    """ Class for let evolve multiple instances of artificial agents """

    def __init__(self, map_shape=(100, 100), population_size=100, generations=100, turns_number=100, own_map=None,
                 initial_position='random',
                 initial_direction='random', network=None,
                 weights_file='coach.h5'):
        self.map = own_map
        if self.map is None:
            self.map = Virtual_Room(map_shape)
        self.generations_number = generations
        self.turns = turns_number
        self.population = []
        if initial_direction == 'random':
            initial_direction = np.random.randint(360)  # all agents on the same direction
        if initial_position == 'random':
            initial_position = (
                np.random.randint(map_shape[0]), np.random.randint(map_shape[1]))  # all agents on the same position
        self.initial_direction = initial_direction
        self.initial_position = initial_position
        for i in range(population_size):  # random population initialization
            self.population.append(Process(
                own_map=self.map.grid,
                initial_position=initial_position,
                initial_direction=initial_direction,
                network=network,
                weights_file=weights_file
            ))

    def training(self, turns=None):
        if turns is None:
            turns = self.turns
        for process in self.population:
            process.learn_rewards()
            process.initial_position = self.initial_position
            process.initial_direction = self.initial_direction
            process.reset_movements()
            process.score = 0
            process.turns = turns
            process.start()
        for process in Process.processes:
            if process.is_alive():
                process.join()
            Process.purge()

    def darwin(self, generations=None, turns_per_generation=None, verbose=1):
        temp = self.population
        if generations is None:
            generations = self.generations_number
        if turns_per_generation is None:
            turns_per_generation = self.turns
        for generation in range(generations):
            if verbose > 0:
                print('Generation {}/{}'.format(generation + 1, generations))
            self.training(turns=turns_per_generation)
            self.population = sorted(self.population)
            self.population[0].save_me()
            print(temp[0])
            if verbose > 0:
                print('Highest score : ', self.population[0].score)
                print('Lowest score : ', self.population[-1].score, '\n')
        if verbose > 1:
            self.population[0].resume_movements()
        return self.population[0]
