#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Q learning agent (opposite to mutative agent) """

# ---- Imports ----
import numpy as np
from keras import models, layers


# ---- Class ----
class Evolutive_Agent:
    """ Agent wich learn by experiment """

    def __init__(self, network=None, weights_file='q_weights.h5'):
        self.net = network
        if self.net is None:
            self.net = self.build_net()
        self.save_file = weights_file
        self.score = 0

    def __lt__(self, other):
        return self.score > other.score

    def save_me(self):
        try:
            self.net.save_weights(self.save_file)
        except OSError:
            self.net.save_weights(self.save_file[:-3] + '1' + '.h5')

    @staticmethod
    def build_net():
        """ Inputs are :
         If obstacle on front
         If unknown area on front
         Amount of greatest reward on front

         Outputs are :
         Turn on left
         Turn on right
         Go forward"""
        model = models.Sequential([
            layers.Dense(9, input_dim=3, activation='relu'),
            layers.Dropout(0.1),
            layers.Dense(54, activation='relu'),
            layers.Dropout(0.1),
            layers.Dense(3, activation='softmax')
        ])
        model.compile(optimizer='adadelta', loss='binary_crossentropy', metrics=['accuracy'])
        model.predict(np.array([[0, 0, 0]]))  # activate model
        return model
