#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Robot Class """

# ---- Imports ----
from ROB4.arduicom import Arduino_Manager
from ROB4.plan_master import Plan_Master
import copy
import numpy as np


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
        data = ""
        while "EOF" not in data:
            data = self.receive_data_line().decode()
            if len(data) > 1 and "EOF" not in data:
                data = data.split(' ')
                temp = {'distance': np.round(float(data[0]), 0), 'angle': int(float(data[1]))}
                measures.append(temp)
        measures = self.filter(measures)
        return measures

    def update_plan(self):
        """ Scale and update the map """
        datas = self.receive_measures()
        self.place_measures(datas=datas)

    def upgrade_plan(self, loop=1):
        """ Loop to increase points  """
        for i in range(loop):
            self.send_permission(permission='measure')
            self.update_plan()

    def filter(self, datas):
        shift = 10
        datas = copy.deepcopy(datas)
        datas = [dico for dico in datas if dico.get('distance', 0) != 0]
        for index in range(len(datas)):
            medium = 0
            tshift = shift
            if index - tshift < 0:
                tshift = index
            if len(datas) <= tshift + index:
                tshift = len(datas) - index - 1
            for i in range(index - tshift, index + tshift + 1):
                medium += datas[i].get('distance')
            medium /= tshift * 2 + 1
            datas[index]['distance'] = medium
        return datas

    def send_permission(self, permission='launch'):
        msg = False
        while not msg:
            self.send_data(permission)
            msg = self.receive_data_line()
