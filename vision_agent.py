#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Description """

# ---- Imports ----
import keras.backend as K
from keras.applications import VGG16
from keras.layers import Flatten, Dense, Dropout
from keras.models import Sequential, Model
from keras.preprocessing.image import load_img, img_to_array
import numpy as np
import os


# ---- Class ----
class Vision_Agent:
    """ Analyze pictures """
    # ---- Settings ----
    default_weights_path = 'weights.h5'

    def __init__(self, shape=(224, 224), depth=3):
        self.shape = shape + (depth,)
        if K.image_data_format() == 'channels_first':  # Theano shape
            self.shape = (depth,) + shape
        self.net = Sequential()  # define net var
        self.buildnet()

    def buildnet(self):
        """ Build the net model """
        self.net = Sequential()
        # prepare base model
        base_model = VGG16(include_top=False,
                           weights='imagenet',
                           input_shape=self.shape)

        # set VGG layers to be not trainable
        for lay in base_model.layers:
            lay.trainable = False

        # prepare the top of the model
        self.net.add(Flatten(input_shape=base_model.output_shape[1:]))
        self.net.add(Dense(256, activation='relu'))
        self.net.add(Dropout(0.10))
        self.net.add(Dense(8, activation='sigmoid'))

        # concatenate both
        self.net = Model(name='tag_image_net', inputs=base_model.input, outputs=self.net(base_model.output))

        # try to load weights excepting file doesn't exist, so it's saved
        try:
            self.net.load_weights(self.default_weights_path)
        except OSError:
            self.net.save_weights(self.default_weights_path, overwrite=True)

        # compile the net
        self.net.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

    def pred_from_dir(self, path):
        """ Makes a prediction from directory path """
        batch = self.prepare_batch(path=path)
        batch = np.array(batch)
        pred = self.net.predict(batch)
        return pred

    def prepare_batch(self, path):
        """ Prepare batch for each directory in the path """
        batch = []
        if os.path.isdir(path):
            images = os.listdir(path)
            for img_path in images:
                if os.path.isdir(os.path.join(path, img_path)):
                    batch += self.prepare_batch(os.path.join(path, img_path))
                try:
                    img = self.extract_picture(os.path.join(path, img_path))
                    batch.append(img)
                except (OSError, FileNotFoundError):
                    continue
        else:
            try:
                batch.append(self.extract_picture(path=path))
            except (OSError, FileNotFoundError):
                return None
        return batch

    def extract_picture(self, path):
        """ Extracts a picture at the path """
        img = load_img(path)
        if K.image_data_format() == 'channels_first':
            img = img.resize(self.shape[1:])
        else:
            img = img.resize(self.shape[:2])
        img = img_to_array(img)
        img = img.reshape(self.shape)
        return img
