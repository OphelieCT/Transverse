#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Main script of project """

import matplotlib.pyplot as plt

# ---- Imports ----
import virtual_room

# ---- Script ----
if __name__ == '__main__':
    room = virtual_room.Virtual_Room((100, 100))
    agent = virtual_room.Artificial_Agent(own_map=room.grid)
    print('Score de départ : {}'.format(agent.score))
    turns = 10 ** 4
    for i in range(turns):
        agent.execute_actions()
        if i % (turns / 10) == 0:
            print('{}) - Score : {}'.format(i, agent.score))
    print('Score final : {}'.format(agent.score))
    plt.scatter(agent.movement_history.get('x'), agent.movement_history.get('y'))
    plt.show()
