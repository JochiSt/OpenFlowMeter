# -*- coding: utf-8 -*-

import sys
sys.path.append("../")
from OpenFlowMeter import OpenFlowMeter
from CANsetup import CANsetup

import time
import numpy as np
import matplotlib.pyplot as plt


def main():

    repetitions = 100            	# repeat how many times
    dac_steps = [10, 32, 64, 128, 256]
    channel = 0                     # which channel to look at

    try:
        # initialise USBtin
        setup = CANsetup()

        # initialise OFM
        ofm =  OpenFlowMeter(usbtin = setup.usbtin, boardID=0x1)

        fig, ax1 = plt.subplots(1, 1)

        for dac in dac_steps:
            print(dac)
            ofm.hasNewMessage = False

            ofm.setDAC(dac, dac)
            time.sleep(2)

            ofm.waitForNewMessage()

            voltage0 = np.array([])
            voltage1 = np.array([])

            current0 = np.array([])
            current1 = np.array([])

            dacs = np.array([])

            for i in range(repetitions):
                ofm.waitForNewMessage()

                voltage0 = np.append( voltage0, ofm.voltage(channel,0))
                voltage1 = np.append( voltage1, ofm.voltage(channel,1))

                current0 = np.append( current0, ofm.current(channel,0))
                current1 = np.append( current1, ofm.current(channel,1))

                dacs = np.append(dacs, dac)

                ofm.hasNewMessage = False

            ax1.plot( dacs, voltage1 / voltage0, label="DAC %d"%(dac), marker=".", linestyle = "")
            ax1.plot( dacs, current1 / current0, label="DAC %d"%(dac), marker=".", linestyle = "")

            voltage0 = voltage0 * 3.3/4095
            voltage1 = voltage1 * 3.3/4095

            current0 = current0 * 3.3/4095 * 10e-3
            current1 = current1 * 3.3/4095 * 10e-3

        ofm.setDAC(0, 0)

        ax1.set_xlabel("measurement point")
        ax1.set_ylabel("voltage / current / LSB / LSB")
        #ax1.legend()

    except:
        pass

    finally:
        setup.deinit()

if __name__ == "__main__":
    main()


