#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Class to launch multiple instances at the same time """

# ---- Imports ----
import threading

from virtual_room.artificial_agent import Artificial_Agent

# ---- Settings ----
lock = threading.RLock()


# ---- Class ----
class Process(threading.Thread, Artificial_Agent):
    """ Thread Agent to launch multiple instances at once """
    processes = []
    results = []

    def __init__(self, own_map=None, initial_position=None, initial_direction=90, network=None,
                 weights_file='mutative.h5', turns=100):
        threading.Thread.__init__(self)
        Artificial_Agent.__init__(self, own_map, initial_position, initial_direction, network=network,
                                  weights_file=weights_file)
        self.turns = turns
        Process.processes.append(self)

    def __del__(self):
        with lock:
            try:
                Process.processes.remove(self)
            except ValueError:
                pass

    def run(self):
        for i in range(self.turns):
            self.execute_actions()
        with lock:
            Process.results.append(self.score)
        return self.score

    @staticmethod
    def purge():
        del Process.results[:]
