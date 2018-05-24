#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Main script of project """

# ---- Imports ----
import ROB4
import os

# ---- Script ----
if __name__ == '__main__':
    mnt_point = '/media/usb0/'
    plan_name = 'plan.png'
    plan_path = os.path.join(mnt_point, plan_name)
    # ROB4.automount(mnt_point, FLAG='Transverse')
    rob = ROB4.Rob(name='Jammy')
    # while True:
    rob.listen()
    # rob.update_plan()
    rob.show_plan()
    # rob.save_plan(plan_path)
