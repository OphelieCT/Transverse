#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Main script of project """

# ---- Imports ----
import virtual_room

# ---- Settings ----
generations = 50
turns = 1000
population = 2
weights = 'training.h5'
map_shape = (10, 10)

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
        weights_file=weights
    )
    finalist = coach.darwin(verbose=2)

    """room = virtual_room.Virtual_Room(_dimensions=map_shape)
    # grid = np.full((map_shape), 0.)
    coord = np.array(map_shape) // 2
    coord = tuple(coord.tolist())
    # grid[coord[0] - 1][coord[1]] = 4.
    # grid[coord[0] - 1][coord[1] - 1] = 5.
    # grid[coord[0] - 1][coord[1] + 1] = virtual_room.Room_Agent.OBSTACLE
    room.grid[coord[0]][coord[1]] = 5.
    test_agent = virtual_room.Room_Agent(own_map=room.grid, initial_position=coord, initial_direction=90)
    print(test_agent.data_on_front())
    print(room)"""
