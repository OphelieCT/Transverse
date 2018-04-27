#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Description """

# ---- Imports ----
import keras.backend as K
from keras.layers import Conv2D, MaxPool2D, Flatten, Dense, Dropout
from keras.models import Sequential


# ---- Class ----
class Vision_Agent:
    """ Analyze pictures """

    def __init__(self, shape=(224, 224), depth=3):
        self.shape = shape + depth
        if K.image_data_format() == 'channels_first':  # Theano shape
            self.shape = depth + shape
        self.net = None  # define net var
        self.buildnet()

    def buildnet(self):
        self.net = Sequential(name='tag_image_net')
        self.net.add(Conv2D(32, (3, 3), input_shape=self.shape, activation='relu'))
        self.net.add(Dropout(0.05))
        self.net.add(MaxPool2D((2, 2)))
        self.net.add(Conv2D(32, (3, 3), activation='relu'))
        self.net.add(Dropout(0.05))
        self.net.add(MaxPool2D((2, 2)))
        self.net.add(Flatten())
        self.net.add(Dense(256, activation='relu'))
        self.net.add(Dropout(0.05))
        self.net.add(Dense(32, activation='softmax'))
        self.net.compile(optimizer='adam', loss='binary_crosstentropy', metrics=['accuracy'])
