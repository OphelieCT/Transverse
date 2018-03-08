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
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense
from keras.preprocessing.image import array_to_img, img_to_array
from keras import losses


# ---- Class ----
class Artificial_Agent(virtual_room.Room_Agent):
    """ Room Agent with artificial intelligence control """

    def __init__(self, shape=(224, 224), _map=None, network=None, depth=1):
        virtual_room.Room_Agent.__init__(self, _map)
        self.score = 0
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
            self.train_to_move()

    def build_net(self):
        self.net = Sequential()
        self.net.add(Conv2D(20, (3, 3), input_shape=self.shape, activation='relu'))
        self.net.add(MaxPooling2D())
        self.net.add(Dropout(0.1))
        self.net.add(Conv2D(20, (3, 3), activation='relu'))
        self.net.add(MaxPooling2D())
        self.net.add(Flatten())
        self.net.add(Dense(256, activation='relu'))
        self.net.add(Dropout(0.1))
        self.net.add(Dense(4, activation='softmax'))
        self.net.compile(optimizer='adadelta', loss=losses.binary_crossentropy, metrics=['accuracy'])

    def prepare_map(self, map_to_convert, pos_x=None, pos_y=None):
        plan = copy.copy(np.array(map_to_convert))
        if pos_x is None:
            pos_x = self.position[0]
        if pos_y is None:
            pos_y = self.position[1]
        plan[pos_x][pos_y] = 0.5
        if K.image_data_format() == 'channels_first':
            dimensions = self.shape[1:]  # prepare dimensions to resize after
            plan = plan.reshape((self.shape[0],) + plan.shape)  # prepare to image conversion
        else:
            dimensions = self.shape[:-1]  # prepare dimensions to resize after
            plan = plan.reshape(plan.shape + (self.shape[-1],))  # prepare to image conversion
        plan = array_to_img(plan)
        plan = plan.resize(dimensions)
        plan.save('test.jpg')
        return img_to_array(plan)

    def choose_action(self):
        """ Movement {0,1,2,3} -> {haut, droite, bas, gauche} """
        plan = self.prepare_map(self.map)
        prediction = self.net.predict(np.array([plan]))[0]
        return prediction

    def train_to_move(self):
        training_map = np.full(self.map.shape, 0.)
        x_train = np.array([
            self.prepare_map(training_map, 0, (len(training_map[0]) - 1) // 2),  # milieu haut
            self.prepare_map(training_map, (len(training_map) - 1) // 2, 0),  # milieu gauche
            self.prepare_map(training_map, len(training_map) - 1, (len(training_map[0]) - 1) // 2),  # milieu bas
            self.prepare_map(training_map, (len(training_map) - 1) // 2, len(training_map[0]) - 1)  # milieu droite
        ])
        predictions = self.net.predict(x_train)
        print(np.round(predictions), '\n')
        x_targets = np.array([
            (0, 1, 0, 0),  # bas
            (0, 0, 1, 0),  # droite
            (0, 0, 0, 1),  # haut
            (1, 0, 0, 0)  # gauche
        ])
        history = self.net.fit(x=x_train, y=x_targets, epochs=10, batch_size=1, verbose=0)
        print(np.round(self.net.predict(x_train)))

    def move(self, next_x=None, next_y=None):
        predictions = tuple(np.round(self.choose_action()))
        next_x, next_y = np.array(self.position) + np.array(self.traductor.get(predictions))
        movement = virtual_room.Room_Agent.move(self, next_x, next_y)

    def collect(self):
        self.score += self.map[self.position[0]][self.position[1]]
        self.map[self.position[0]][self.position[1]] = 0.
