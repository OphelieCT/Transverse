#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Manage storage """

# ---- Imports ----
import os
import glob
import subprocess
import time


# ---- Functions ----
def automount(mnt_point, FLAG='Transverse'):
    path = '/dev/sd*'
    old_devices = glob.glob(path)
    while True:
        devices = glob.glob(path)
        if devices != old_devices:
            old_devices = devices
            for dev in devices:
                if 'sd' in dev:
                    p = subprocess.Popen("mount {0} {1}".format(dev, mnt_point), shell=True,
                                         stdout=subprocess.PIPE,
                                         stderr=subprocess.PIPE)
                    tlist = os.listdir(mnt_point)
                    if FLAG not in tlist:
                        p = subprocess.Popen('umount {0}'.format(mnt_point), shell=True,
                                             stdout=subprocess.PIPE,
                                             stderr=subprocess.PIPE)
                    else:
                        return
        time.sleep(1)
