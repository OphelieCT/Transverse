#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Class wich trains artificial agents and let them evolve """

import copy

# ---- Imports ----
from virtual_room import Process, Virtual_Room, Mutative_Agent


# ---- Class ----
class Artificial_Coach:
    """ Class for let evolve multiple instances of artificial agents """

    def __init__(self, population_size=100, generations=100, turns_number=100, own_map=None, initial_position='random',
                 initial_direction='random', network=None,
                 weights_file='mutative.h5'):
        self.map = own_map
        if self.map is None:
            self.map = Virtual_Room((100, 100))
        self.generations_number = generations
        self.turns = turns_number
        temp_map = copy.deepcopy(self.map.grid)  # keep original map safe
        self.population = []
        for i in range(population_size):  # random population initialization
            self.population.append(Process(
                own_map=temp_map,
                initial_position=initial_position,
                initial_direction=initial_direction,
                network=network,
                weights_file=weights_file
            ))

    def training(self, turns=None):
        if turns is None:
            turns = self.turns
        for process in self.population:
            process.start(turns)
        for process in self.population:
            process.join()
        self.population = Mutative_Agent.evolve_population(self.population, winner_percentage=0.3, other_percentage=0.1)

    def darwin(self, generations=None, turns_per_generation=None, verbose=1):
        if generations is None:
            generations = self.generations_number
        if turns_per_generation is None:
            turns_per_generation = self.turns
        for generation in range(generations):
            for process in self.population:
                process.reset_movements()
            if verbose > 0:
                print('Generation {}/{}'.format(generation + 1, generations))
            self.training(turns=turns_per_generation)
