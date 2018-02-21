#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Lab main script of project """

# ---- Imports ----
import keras.backend as K
from keras.models import Model
from keras.layers import Dense
from keras.applications import VGG16
from keras.preprocessing.image import img_to_array, ImageDataGenerator
from PIL.Image import Image

# ---- Script ----
if __name__ == '__main__':
    datagen = ImageDataGenerator(
        rescale=1. / 255
    )
