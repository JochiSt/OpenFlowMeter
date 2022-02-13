# -*- coding: utf-8 -*-

import sys
sys.path.append("../")
from OpenFlowMeter import OpenFlowMeter
from CANsetup import CANsetup
from PlotData import plotVoltageVsDAC, plotCurrentVsDAC, plotResistanceVsDAC
from Measurements import DACsweep

import time

import numpy as np

def main():
    # initialise USBtin
    setup = CANsetup()

    # initialise OFM
    ofm =  OpenFlowMeter(usbtin = setup.usbtin, boardID=0x1)

    measurement_successful = False

    # configuration
    channels = [0,1]      # channels, we want to analyse
    steps = 32              # how many steps do we want to have

    try:
        dac, voltage, current = DACsweep(ofm=ofm, channel=channels, steps = steps)
        measurement_successful = True
    except Exception as e:
        print(e)
        pass

    setup.deinit()

    if not measurement_successful:
        return

    # convert from ADC LSB into SI
    for chan in channels:
        voltage[chan] = 3.3/4095 * voltage[chan]
        current[chan] = 3.3/4095 * current[chan] * 10e-3    # from simulation 1V = 10mA

    # save recorded data in NPZ files
    for chan in channels:
        np.savez("measurement_%s_CH%d_%d.npz"%(time.strftime("%Y%m%d_%H%M%S"),
                                               chan, steps),
                        dac=dac[chan], voltage=voltage[chan], current=current[chan])

    plotCurrentVsDAC(dac[0], current[0])
    plotResistanceVsDAC(dac[0], voltage[0], current[0])

if __name__ == "__main__":
    main()


