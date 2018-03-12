#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Class to launch multiple instances at the same time """

# ---- Imports ----
import threading

from virtual_room import Artificial_Agent

# ---- Settings ----
lock = threading.RLock()


# ---- Class ----
class Process(threading.Thread, Artificial_Agent):
    """ Thread Agent to launch multiple instances at once """
    processes = []
    results = []

    def __init__(self, own_map=None, initial_position=None, initial_direction=90, network=None,
                 weights_file='mutative.h5'):
        threading.Thread.__init__(self)
        Artificial_Agent.__init__(self, own_map, initial_position, initial_direction, network, weights_file)
        Process.processes.append(self)

    def __del__(self):
        with lock:
            Process.processes.remove(self)

    def run(self, turn_numbers=100):
        for i in range(turn_numbers):
            self.execute_actions()
        with lock:
            Process.results.append(self.score)
        return self.score

    @staticmethod
    def purge():
        del Process.results[:]
