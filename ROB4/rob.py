#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Robot Class """

# ---- Imports ----
from ROB4.arduicom import Arduino_Manager
from ROB4.plan_master import Plan_Master


# ---- Class ----
class Rob(
    Arduino_Manager,
    Plan_Master
):
    """ A class which define robot """

    def __init__(self, name="", position=(0, 0), direction=0, shape=(1, 1), port=None):
        Arduino_Manager.__init__(self, port=port)
        Plan_Master.__init__(self, position=position, direction=direction, shape=shape)
        self.name = name

    def receive_measures(self):
        """ Get measures per lines from arduino board """
        measures = []
        data = True
        while data:
            data = self.receive_data_line()
            data = data.split(' ')
            measures.append({'distance': data[0] * 340 / 20000, 'angle': data[1]})
        return measures

    def update_plan(self):
        """ Scale and update the map """
        datas = self.receive_measures()
        self.place_measures(datas=datas)
