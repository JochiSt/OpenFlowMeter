# -*- coding: utf-8 -*-

import sys
sys.path.append("../")
from OpenFlowMeter import OpenFlowMeter

from CANsetup import CANsetup
from Measurements import StabilityTest

import time

import numpy as np

def main():
    try:
        # initialise USBtin
        setup = CANsetup()

        # initialise OFM
        ofm =  OpenFlowMeter(usbtin = setup.usbtin, boardID=0x1)

        measurement_successful = False

        # configuration
        channels = [0,1]            # channels, we want to analyse
        repetitions = 10            # repeat how many times

        dac_steps = [0, 32, 512, 1024] #, 64, 96, 128]


        for dac in dac_steps:
            print(dac)
            ofm.setDAC(dac, dac)

            ofm.waitForNewMessage()

            voltage0 = np.array([ ofm.voltage(0,0), ofm.voltage(0,1) ])
            voltage1 = np.array([ ofm.voltage(1,0), ofm.voltage(1,1) ])

            current0 = np.array([ ofm.current(0,0), ofm.current(0,1) ])
            current1 = np.array([ ofm.current(1,0), ofm.current(1,1) ])

            voltage0 = voltage0 * 3.3/4095
            voltage1 = voltage1 * 3.3/4095


            current0 = current0 * 3.3/4095 * 10e-3
            current1 = current1 * 3.3/4095 * 10e-3

            print("U", voltage0, voltage1)
            print("I", current0, current1)

            print("R", voltage0/current0, voltage1/current1)

        ofm.setDAC(0, 0)

    except:
        pass

    finally:
        setup.deinit()

if __name__ == "__main__":
    main()


