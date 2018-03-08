#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" A Room Agent with AI """

# ---- Imports ----
import virtual_room
import time
import numpy as np
import copy
import keras.backend as K
from keras.models import Sequential
from keras.layers import Conv2D, MaxPooling2D, Dropout, Flatten, Dense
from keras.preprocessing.image import array_to_img, img_to_array


# ---- Class ----
class Artificial_Agent(virtual_room.Room_Agent):
    """ Room Agent with artificial intelligence control """

    def __init__(self, shape=(224, 224), _map=None, network=None):
        virtual_room.Room_Agent.__init__(self, _map)
        self.score = 0
        self.net = network
        self.shape = shape + (1,)
        if K.image_data_format() == 'channels_first':
            self.shape = (1,) + shape

        if self.net is None:
            self.build_net()

    def build_net(self):
        self.net = Sequential()
        self.net.add(Conv2D(8, (3, 3), input_shape=self.shape, activation='relu'))
        self.net.add(MaxPooling2D())
        self.net.add(Dropout(0.1))
        self.net.add(Conv2D(8, (3, 3), activation='relu'))
        self.net.add(MaxPooling2D())
        self.net.add(Flatten())
        self.net.add(Dense(16, activation='relu'))
        self.net.add(Dropout(0.1))
        self.net.add(Dense(4, activation='softmax'))
        self.net.compile(optimizer='adadelta', loss='binary_crossentropy', metrics=['accuracy'])

    def choose_action(self):
        """ Movement {0,1,2,3} -> {haut, droite, bas, gauche} """
        plan = copy.copy(np.array(self.map))
        plan[self.position[0]][self.position[1]] = 0.5
        if K.image_data_format() == 'channels_first':
            dimensions = self.shape[1:]  # prepare dimensions to resize after
            plan = plan.reshape((1,) + plan.shape)  # prepare to image conversion
        else:
            dimensions = self.shape[:-1]  # prepare dimensions to resize after
            plan = plan.reshape(plan.shape + (1,))  # prepare to image conversion
        plan = array_to_img(plan)
        plan = plan.resize(dimensions)

        plan = img_to_array(plan)
        prediction = self.net.predict(np.array([plan]))[0]
        return prediction

    def move(self, next_x=None, next_y=None):
        traductor = {
            (0, 0, 0, 1): [-1, 0],  # haut
            (0, 0, 1, 0): [0, 1],  # droite
            (0, 1, 0, 0): [1, 0],  # bas
            (1, 0, 0, 0): [0, -1],  # gauche
        }
        predictions = tuple(np.round(self.choose_action()))
        next_x, next_y = np.array(self.position) + np.array(traductor.get(predictions))
        movement = virtual_room.Room_Agent.move(self, next_x, next_y)
