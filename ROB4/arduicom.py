#!/usr/bin/python3
# coding: utf-8

# ---- Description ----
""" Arduino communication """

# ---- Imports ----
import serial
import sys
import glob


# ---- Class ----
class Arduino_Manager:
    """ Manage communication with arduino board """

    def __init__(self, port=None):
        if port is None:
            port = self.serial_ports()[0]
        self.port = serial.Serial(port=port, baudrate=9600, timeout=1)

    def send_data(self, data: str):
        self.port.write(data.encode())

    def receive_data_line(self):
        return self.port.readline()

    @staticmethod
    def serial_ports():
        """ Lists serial port names

            :raises EnvironmentError:
                On unsupported or unknown platforms
            :returns:
                A list of the serial ports available on the system
        """
        if sys.platform.startswith('win'):
            ports = ['COM%s' % (i + 1) for i in range(256)]
        elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
            # this excludes your current terminal "/dev/tty"
            ports = glob.glob('/dev/tty[A-Za-z]*')
        elif sys.platform.startswith('darwin'):
            ports = glob.glob('/dev/tty.*')
        else:
            raise EnvironmentError('Unsupported platform')

        result = []
        for port in ports:
            try:
                s = serial.Serial(port)
                s.close()
                result.append(port)
            except (OSError, serial.SerialException):
                pass
        return result
