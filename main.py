#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Main script of project """

import numpy as np

# ---- Imports ----
import virtual_room

# ---- Settings ----
generations = 50
turns = 1000
population = 2
weights = 'training.h5'
map_shape = (3, 3)

# ---- Script ----
if __name__ == '__main__':
    """coach = virtual_room.Artificial_Coach(
        map_shape=map_shape,
        population_size=population,
        generations=generations,
        turns_number=turns,
        own_map=None,
        initial_position='random',
        initial_direction='random',
        network=None,
        weights_file=weights
    )
    finalist = coach.darwin(verbose=2)
"""
    grid = np.full((map_shape), 0.)
    coord = np.array(map_shape) // 2
    coord = tuple(coord.tolist())
    grid[coord[0] - 1][coord[1]] = 1.
    grid[coord[0]][coord[1]] = 5.
    test_agent = virtual_room.Room_Agent(own_map=grid, initial_position=coord, initial_direction=90)
    print(grid[0][1], ' ', grid[1][1])
    print(test_agent.data_on_front())
    print(grid)
