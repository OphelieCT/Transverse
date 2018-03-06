#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" An agent wich explore the room and try to map it """


# ---- Imports ----


# ---- Class ----
class Room_Agent:
    """ An agent wich explore the room and try to map it """
    general_id = 0

    def __init__(self):
        self.id = Room_Agent.general_id
        Room_Agent.general_id += 1

        self.map = []
