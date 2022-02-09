# -*- coding: utf-8 -*-
"""
Created on Wed Feb  9 08:42:40 2022

@author: steinmann
"""

import sys
sys.path.append("../pyUSBtin")

from pyusbtin.usbtin import USBtin
from pyusbtin.canmessage import CANMessage
from time import sleep

def log_data(msg):
    print(msg)

usbtin = USBtin()
usbtin.connect("COM7")
usbtin.add_message_listener(log_data)
usbtin.open_can_channel(500000, USBtin.ACTIVE)

while(True):
    print("tick")
    #usbtin.send(CANMessage(0x100, "\x11"))
    sleep(1)
