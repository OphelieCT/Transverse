#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Main script of project """

# ---- Imports ----
import virtual_room

# ---- Settings ----
generations = 100
turns = 1000
population = 5
weights = 'training.h5'
map_shape = (10, 10)
mutation_rate = 0

# ---- Script ----
if __name__ == '__main__':
    coach = virtual_room.Artificial_Coach(
        map_shape=map_shape,
        population_size=population,
        generations=generations,
        turns_number=turns,
        own_map=None,
        initial_position='random',
        initial_direction='random',
        network=None,
        weights_file=weights,
        mutation_rate=mutation_rate
    )
    finalist = coach.darwin(verbose=2)
