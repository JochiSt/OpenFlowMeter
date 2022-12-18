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

    dac_steps = np.array([])

    DAC_START = 0
    DAC_STOP  = 64
    DAC_STEP  = 2

    dac_steps = np.append(dac_steps,
                      np.linspace(DAC_START, DAC_STOP, int( (DAC_STOP - DAC_START)/DAC_STEP +1) ))



    DAC_START = 64
    DAC_STOP  = 1024
    DAC_STEP  = 64

    dac_steps = np.append(dac_steps,
                          np.linspace(DAC_START, DAC_STOP, int( (DAC_STOP - DAC_START)/DAC_STEP +1) ))

    channel = 1  # which channel to look at

    try:
        # initialise USBtin
        setup = CANsetup()

        # initialise OFM
        ofm =  OpenFlowMeter(usbtin = setup.usbtin, boardID=0x1)

        fig, (ax1, ax2) = plt.subplots(1, 2)

        voltage0 = np.array([])
        voltage1 = np.array([])

        current0 = np.array([])
        current1 = np.array([])

        dacs = np.array([])

        for dac in dac_steps:
            print(dac)

            ofm.setDAC(int(dac), int(dac) )

            time.sleep(2)
            ofm.hasNewMessage = False
            ofm.waitForNewMessage()

            for i in range(repetitions):
                ofm.waitForNewMessage()

                voltage0 = np.append( voltage0, ofm.voltage(channel,0))
                voltage1 = np.append( voltage1, ofm.voltage(channel,1))

                current0 = np.append( current0, ofm.current(channel,0))
                current1 = np.append( current1, ofm.current(channel,1))

                dacs = np.append(dacs, dac)

                ofm.hasNewMessage = False

        ofm.setDAC(0, 0)

        ax1.plot( dacs, voltage1 / voltage0, label="voltage", marker=".", linestyle = "-")
        ax1.plot( dacs, current1 / current0, label="curent", marker=".", linestyle = "-")

        ax2.plot(dacs, voltage0, label="voltage 0", marker=".", linestyle = "-")
        ax2.plot(dacs, voltage1, label="voltage 1", marker=".", linestyle = "-")
        ax2.plot(dacs, current0, label="current 0", marker=".", linestyle = "-")
        ax2.plot(dacs, current1, label="current 1", marker=".", linestyle = "-")

        """
        voltage0 = voltage0 * 3.3/4095 # 1 LSB = 0,8 mV
        voltage1 = voltage1 * 3.3/4095

        current0 = current0 * 3.3/4095 * 10e-3 # 1 LSB = 8 uA
        current1 = current1 * 3.3/4095 * 10e-3
        """

        ax1.set_title("voltage & current gain")
        ax1.set_xlabel("DAC setpoint LSB")
        ax1.set_ylabel("LSB gain")
        ax1.legend()

        ax2.set_title("voltage & current response")
        ax2.set_xlabel("DAC setpoint LSB")
        ax2.set_ylabel("current / voltage / LSB")
        ax2.legend()

        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.show()

        fig, (ax1) = plt.subplots(1, 1)
        ax1.plot(dacs, voltage0 / current0, label="gain 0", marker=".", linestyle = "-" )
        ax1.plot(dacs, voltage1 / current1, label="gain 1", marker=".", linestyle = "-" )
        ax1.legend()

        fig.tight_layout()  # otherwise the right y-label is slightly clipped
        plt.show()

        np.savez("stability_v2_%s_CH%d_%d.npz"%(time.strftime("%Y%m%d_%H%M%S"), channel, repetitions),
                        voltage0 = voltage0, current0=current0,
                        voltage1 = voltage1, current1=current1,
                        dacs=dacs)

    except Exception as e:
        print(e)
        pass

    finally:
        setup.deinit()

if __name__ == "__main__":
    main()


