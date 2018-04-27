#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Main script of project """

# ---- Imports ----
from vision_agent import Vision_Agent

# ---- Settings ----
path = 'C:\\Users\\MPuis\\PycharmProjects\\Transverse\\pictures'

# ---- Script ----
if __name__ == '__main__':
    net = Vision_Agent()
    for pred in net.pred_from_pict(path=path):
        print(pred, '\n')
