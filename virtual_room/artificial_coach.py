#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Class wich trains artificial agents and let them evolve """

# ---- Imports ----
import threading

from virtual_room import Artificial_Agent

# ---- Settings ----
lock = threading.RLock()


# ---- Class ----
class Process(threading.Thread, Artificial_Agent):
    """ Trainer for artificial agent population """
    id = 0
    processes = 0
    results = 0

    def __init__(self, turn_number=100, own_map=None, initial_position=None, initial_direction=90, network=None,
                 weights_file='mutative.h5'):
        threading.Thread.__init__(self)
        Artificial_Agent.__init__(self, own_map, initial_position, initial_direction, network, weights_file)
