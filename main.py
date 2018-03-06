#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Main script of project """

# ---- Imports ----
import virtual_room

# ---- Script ----
if __name__ == '__main__':
    lab = virtual_room.Virtual_Room((5, 5))
    agent = virtual_room.Room_Agent()
    print(agent.id)
    lab.represent()
