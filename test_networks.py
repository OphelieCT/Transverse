#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Main script of project """

# ---- Imports ----
import virtual_room

# ---- Settings ----
generations = 100
turns = 100
population = 10
weights = 'training.h5'
map_shape = (100, 100)

# ---- Script ----
if __name__ == '__main__':
    room = virtual_room.Virtual_Room(map_shape)
    agent = virtual_room.Artificial_Agent(own_map=room.grid, initial_position=(0, 0), initial_direction=90)
    agent.net.load_weights(weights)
    print('Initial score : ', agent.score)
    for i in range(turns):
        agent.execute_actions()
    print('Final score :', agent.score)
    print(agent.movement_history)
    agent.resume_movements()
