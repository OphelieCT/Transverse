#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" A Room Agent with AI """

import keras.backend as K
import numpy as np
from keras import losses
from keras.layers import Dropout, Dense
from keras.models import Sequential

# ---- Imports ----
from researches.virtual_room import Room_Agent


# ---- Class ----
class Convolutional_Agent(Room_Agent):
    """ Room Agent with artificial intelligence control """

    def __init__(self, shape=(224, 224), own_map=None, network=None, depth=1, save_file='test.h5', base_position=None):
        Room_Agent.__init__(self, own_map)
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
            except (OSError, ValueError):
                self.train_to_move()

    def build_net(self):
        self.net = Sequential([
            Dense(20, input_dim=4, activation='relu'),
            Dropout(0.2),
            Dense(16, activation='relu'),
            Dropout(0.2),
            Dense(4, activation='softmax')
        ])
        self.net.compile(optimizer='adadelta', loss=losses.binary_crossentropy, metrics=['accuracy'])

    def prepare_batch(self, special_map=None, pos_x=None, pos_y=None):
        if special_map is None:
            special_map = self.map
        if pos_x is None:
            pos_x = self.position[0]
        if pos_y is None:
            pos_y = self.position[1]
        temp = []
        height = 1
        width = 1
        for i in range(-height, height + 1):
            for j in range(-width, width + 1):
                if i ** 2 != j ** 2:
                    if 0 <= (pos_x + i) < len(special_map) and 0 <= (pos_y + j) < len(special_map[0]):
                        temp.append(special_map[pos_x + i][pos_y + j])
                    else:
                        temp.append(1.)
        temp = np.array(temp)
        return temp

    def choose_action(self):
        """ Movement {0,1,2,3} -> {haut, droite, bas, gauche} """
        plan = self.prepare_batch()
        prediction = self.net.predict(np.array([plan]))[0]
        return prediction

    def train_to_move(self):
        training_map = np.full(self.map.shape, 0.)
        x_train = np.array([
            self.prepare_batch(training_map, 0, len(training_map[0]) // 2),  # milieu haut
            self.prepare_batch(training_map, len(training_map) // 2, len(training_map[0]) - 1),  # milieu droite
            self.prepare_batch(training_map, len(training_map) - 1, len(training_map[0]) // 2),  # milieu bas
            self.prepare_batch(training_map, len(training_map) // 2, 0)  # milieu gauche
        ])
        x_targets = np.array([
            (0, 1, 0, 0),  # bas
            (1, 0, 0, 0),  # gauche
            (0, 0, 0, 1),  # haut
            (0, 0, 1, 0),  # droite
        ])
        history = self.net.fit(x=x_train, y=x_targets, epochs=1000, batch_size=1, verbose=0)
        while True:
            try:
                self.net.save_weights(self.save_file)
                break
            except OSError:
                self.save_file = self.save_file[:-3] + '1' + '.h5'

    def move(self, next_x=None, next_y=None):
        predictions = tuple(np.round(self.choose_action()))
        next_x, next_y = np.array(self.position) + np.array(self.traductor.get(predictions))
        if Room_Agent.move(self, next_x, next_y) == 0:
            self.movement_history['x'].append(next_x)
            self.movement_history['y'].append(next_y)

    def collect(self):
        self.score += self.map[self.position[0]][self.position[1]]
        self.map[self.position[0]][self.position[1]] = 0.
