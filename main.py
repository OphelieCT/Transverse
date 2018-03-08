#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Main script of project """

# ---- Imports ----
import virtual_room

# ---- Script ----
if __name__ == '__main__':
    room = virtual_room.Virtual_Room((1000, 1000))
    agent = virtual_room.Artificial_Agent(_map=room.grid)
