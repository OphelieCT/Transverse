#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" An agent with neural network wich can mutate """

# ---- Imports ----
import numpy as np
from keras import models, layers

# ---- Settings ----
np.random.seed()


# ---- Class ----
class Mutative_Agent:
    """ An agent with neural network wich can mutate """

    def __init__(self, network=None, weights_file='mutative.h5'):
        self.score = 0
        self.weights_file = weights_file
        self.net = network
        if self.net is None:
            self.net = self.build_net()

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
        return model

    def mutation(self):
        """ Create second neural network and mix both with 1/10 variation """
        temp = [self.net] * 9 + [self.build_net()]
        self.net = self.cross(temp)

    @staticmethod
    def cross(networks):
        """ Mix each network in list with the first layer by layer """
        if type(networks) not in (tuple, list, np.ndarray):
            return None
        try:
            temp_net = networks[0]
            for i in range(1, len(networks)):
                for j in range(len(temp_net.layers)):
                    temp_weights = temp_net.layers[j].get_weights()
                    input_weights = networks[i].layers[j].get_weights()
                    for _ in range(len(temp_weights)):
                        temp_weights[_] += input_weights[_]
                        temp_weights[_] /= len(networks)
                    temp_net.layers[j].set_weights(temp_weights)
        except ValueError:
            return None
        return temp_net
