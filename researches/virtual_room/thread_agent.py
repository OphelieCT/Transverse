#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Class to launch multiple instances at the same time """

# ---- Imports ----
import threading

from researches.virtual_room.artificial_agent import Artificial_Agent


# ---- Class ----
class Process(Artificial_Agent):
    """ Thread Agent to launch multiple instances at once """
    processes = []
    results = []

    def __init__(self, own_map=None, initial_position=None, initial_direction=90, network=None,
                 weights_file='mutative.h5', turns=100, mutation_rate=30):
        Artificial_Agent.__init__(self, own_map=own_map, initial_position=initial_position,
                                  initial_direction=initial_direction, network=network, weights_file=weights_file)
        self.turns = turns

    def execute_thread(self):
        for i in range(self.turns):
            self.execute_actions()

    def start(self):
        self.known = []
        temp = threading.Thread(target=Process.execute_thread, args=(self,))
        temp.start()
        Process.processes.append(temp)

    @staticmethod
    def purge():
        del Process.results[:]
