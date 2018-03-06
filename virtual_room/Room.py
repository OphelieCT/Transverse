#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" A virtual room where we can test every algorithms """

# ---- Imports ----
import numpy as np

# ---- Some setups ----
np.random.seed()


# ---- Class ----
class Virtual_Room:
    """ A virtual room to experiment some tests """

    def __init__(self, _dimensions: tuple):
        self.dimensions = _dimensions
        self.grid = None
        self.create_grid()

    def create_grid(self):
        self.grid = np.random.randint(0, 1, size=self.dimensions)
