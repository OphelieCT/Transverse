#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Class wich trains artificial agents and let them evolve """

import copy

# ---- Imports ----
from virtual_room import Process, Virtual_Room


# ---- Class ----
class Artificial_Coach:
    """ Class for let evolve multiple instances of artificial agents """

    def __init__(self, population_size=100, turns_number=100, own_map=None, initial_position='random',
                 initial_direction='random', network=None,
                 weights_file='mutative.h5'):
        self.map = own_map
        if self.map is None:
            self.map = Virtual_Room((100, 100))
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

    def training(self):
        for processus in self.population:
            processus.start(self.turns)
        for processus in self.population:
            processus.join()
