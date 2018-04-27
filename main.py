#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Main script of project """

# ---- Imports ----
from vision_agent import Vision_Agent
import numpy as np

# ---- Settings ----
path = 'C:\\Users\\MPuis\\PycharmProjects\\Transverse\\pictures'

# ---- Script ----
if __name__ == '__main__':
    net = Vision_Agent()
    predictions: np.ndarray = net.pred_from_dir(path=path)
    predictions = predictions * 10 ** 1
    predictions = predictions.astype(int)
    for pred in predictions:
        for second_pred in predictions:
            if pred is not second_pred:
                print(np.array_equal(pred, second_pred))
        print(pred, '\n')
