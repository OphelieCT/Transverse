#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Main script of project """

# ---- Imports ----
import ROB4
import time
import os

# ---- Script ----
if __name__ == '__main__':
    rob = ROB4.Rob(name='Jammy')
    scan_latence = 10
    mnt_point = '/media/usb0/'
    plan_name = 'plan.png'
    plan_path = os.path.join(mnt_point, plan_name)
    ROB4.automount(mnt_point, FLAG='Transverse')
    while True:
        rob.upgrade_plan(2)
        rob.save_plan(plan_path)
        time.sleep(scan_latence)
