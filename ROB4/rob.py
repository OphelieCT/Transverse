#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Robot Class """

# ---- Imports ----
from ROB4.arduicom import Arduino_Manager
from ROB4.plan_master import Plan_Master
import copy
import numpy as np
import time


# ---- Class ----
class Rob(
    Arduino_Manager,
    Plan_Master
):
    """ A class which define robot """
    ending_msg = 'EOF'

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
            if len(data) > 1 and self.ending_msg not in data:
                data = data.split(' ')
                temp = {'distance': np.round(float(data[0]), 0), 'angle': int(float(data[1]))}
                measures.append(temp)
        measures = self.filter(measures)
        return measures

    def update_plan(self):
        """ Scale and update the map """
        datas = self.receive_measures()
        self.place_measures(datas=datas)

    def upgrade_plan(self):
        """ Loop to increase points  """
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

    def listen(self):
        while True:
            msg = self.receive_data_line().decode()
            if 'left' in msg:
                self.direction += 360 - 90
                self.direction %= 360
            elif 'right' in msg:
                self.direction += 90
                self.direction %= 360
            elif 'permission_needed' in msg:
                self.upgrade_plan()
            else:
                time.sleep(1)
                continue
            break

    def send_permission(self, permission='launch'):
        msg = self.receive_data_line()
        while "permission_needed" not in msg.decode():
            self.send_data(permission)
            msg = self.receive_data_line()
        while "permission_needed" in msg.decode():
            self.send_data(permission)
            msg = self.receive_data_line()
