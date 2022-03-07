# -*- coding: utf-8 -*-

import sys
sys.path.append("LabDeviceControl")
import LabDeviceControl

class DMMsetup(object):
    def __init__(self, COMport="COM9"):
        self.dmm = LabDeviceControl.PeakTech_DMM3315()
        self.dmm.connect(COMport)

    def deinit(self):
        # shutting down interface to DMM
        self.dmm.stop_rx_thread()
        # disconnect from USBtin
        self.dmm.disconnect()
