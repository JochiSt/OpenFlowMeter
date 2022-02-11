# -*- coding: utf-8 -*-
"""

"""
import sys
sys.path.append("pyUSBtin")
from pyusbtin.usbtin import USBtin
from pyusbtin.canmessage import CANMessage

class CANsetup(object):
    def __init__(self, COMport="COM7"):
        self.usbtin = USBtin()
        self.usbtin.connect(COMport)
        self.usbtin.open_can_channel(500000, USBtin.ACTIVE)

    def deinit(self):
        # shutting down CAN interface
        self.usbtin.stop_rx_thread()
        self.usbtin.close_can_channel()
        # disconnect from USBtin
        self.usbtin.disconnect()