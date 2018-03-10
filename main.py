#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Main script of project """

# ---- Imports ----
import virtual_room
import matplotlib.pyplot as plt

# ---- Script ----
if __name__ == '__main__':
    room = virtual_room.Virtual_Room((1000, 1000))
    agent = virtual_room.Artificial_Agent(_map=room.grid)
    print('Score de départ : {}'.format(agent.score))
    turns = 10 ** 4
    for i in range(turns):
        agent.move()
        agent.collect()
        if i % (turns / 10) == 0:
            print('{}) - Score : {}'.format(i, agent.score))
    print('Score final : {}'.format(agent.score))
    plt.scatter(agent.movement_history.get('x'), agent.movement_history.get('y'))
    plt.show()
