#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Main script of project """

# ---- Imports ----
import ROB4
import time

# ---- Script ----
if __name__ == '__main__':
    rob = ROB4.Rob(name='Jammy')
    scan_latence = 10
    while True:
        rob.upgrade_plan(2)
        rob.save_plan('/media/usb0/plan.png')
        time.sleep(scan_latence)
