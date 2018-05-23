#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Main script of project """

# ---- Imports ----
import ROB4
import os

# ---- Script ----
if __name__ == '__main__':
    rob = ROB4.Rob(name='Jammy')
    mnt_point = '/media/usb0/'
    plan_name = 'plan.png'
    plan_path = os.path.join(mnt_point, plan_name)
    ROB4.automount(mnt_point, FLAG='Transverse')
    while True:
        rob.listen()
        rob.save_plan(plan_path)
