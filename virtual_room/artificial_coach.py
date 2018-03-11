#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Class wich trains artificial agents and let them evolve """


# ---- Imports ----

# ---- Class ----
class Articial_Coach:
    """ Trainer for artificial agent population """

    def __init__(self, own_map, population_size, mutation_rate=30):
        self.pop_size = population_size
        self.mutation_rate = mutation_rate
        self.map = own_map
