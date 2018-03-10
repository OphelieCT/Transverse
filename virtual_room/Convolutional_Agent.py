#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" A Room Agent with AI """

# ---- Imports ----
import virtual_room
import time
import matplotlib.pyplot as plt
import numpy as np
import copy
import keras.backend as K
from keras.models import Sequential
from keras.layers import Dropout, Dense
from keras import losses


# ---- Class ----
class Artificial_Agent(virtual_room.Room_Agent):
    """ Room Agent with artificial intelligence control """

    def __init__(self, shape=(224, 224), _map=None, network=None, depth=1, save_file='test.h5', base_position=None):
        virtual_room.Room_Agent.__init__(self, _map)
        self.position = base_position
        if base_position is None:
            self.position = (len(self.map) // 2, len(self.map[0]) // 2)
        self.score = 0
        self.movement_history = {'x': [], 'y': []}
        self.save_file = save_file
        self.net = network
        self.traductor = {
            (0, 0, 0, 1): [-1, 0],  # haut
            (0, 0, 1, 0): [0, 1],  # droite
            (0, 1, 0, 0): [1, 0],  # bas
            (1, 0, 0, 0): [0, -1],  # gauche
        }
        self.shape = shape + (depth,)
        if K.image_data_format() == 'channels_first':
            self.shape = (depth,) + shape
        if self.net is None:
            self.build_net()
            try:
                self.net.load_weights(save_file)
            except OSError:
                self.train_to_move()

    def build_net(self):
        self.net = Sequential([
            Dense(20, input_dim=4, activation='relu'),
            Dropout(0.2),
            Dense(40, activation='relu'),
            Dropout(0.2),
            Dense(4, activation='softmax')
        ])
        self.net.compile(optimizer='adadelta', loss=losses.binary_crossentropy, metrics=['accuracy'])

    def prepare_batch(self, pos_x=None, pos_y=None):
        if pos_x is None:
            pos_x = self.position[0]
        if pos_y is None:
            pos_y = self.position[1]
        temp = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if i ** 2 != j ** 2:
                    try:
                        temp.append(self.map[pos_x + i][pos_y + j])
                    except IndexError:
                        temp.append(1.)
        return temp

    def choose_action(self):
        """ Movement {0,1,2,3} -> {haut, droite, bas, gauche} """
        plan = self.prepare_batch()
        prediction = self.net.predict(np.array([plan]))[0]
        return prediction

    def train_to_move(self):
        training_map = np.full(self.map.shape, 0.)
        x_train = np.array([
            (0, 0, 0, 1),  # milieu haut
            (0, 0, 1, 0),  # milieu droite
            (0, 1, 0, 0),  # milieu bas
            (1, 0, 0, 0)  # milieu gauche
        ])
        predictions = self.net.predict(x_train)
        x_targets = np.array([
            (0, 1, 0, 0),  # bas
            (1, 0, 0, 0),  # gauche
            (0, 0, 0, 1),  # haut
            (0, 0, 1, 0),  # droite
        ])
        history = self.net.fit(x=x_train, y=x_targets, epochs=1000, batch_size=1, verbose=0)
        self.net.save_weights(self.save_file)

    def move(self, next_x=None, next_y=None):
        predictions = tuple(np.round(self.choose_action()))
        next_x, next_y = np.array(self.position) + np.array(self.traductor.get(predictions))
        if virtual_room.Room_Agent.move(self, next_x, next_y) == 0:
            self.movement_history['x'].append(next_x)
            self.movement_history['y'].append(next_y)

    def collect(self):
        self.score += self.map[self.position[0]][self.position[1]]
        self.map[self.position[0]][self.position[1]] = 0.
