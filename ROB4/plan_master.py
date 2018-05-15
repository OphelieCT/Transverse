#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Map management """

# ---- Imports ----
import copy
import numpy as np
import matplotlib.pyplot as plt


# ---- Class ----
class Plan_Master:
    """ Create and manage maps """
    freeway = 0
    obstacle = 1
    unknown = -1

    def __init__(self, position=(0, 0), direction=0, shape=(1, 1)):
        self.plan = np.full(shape, Plan_Master.freeway).tolist()
        self.position = position
        self.direction = direction
