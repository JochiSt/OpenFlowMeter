# -*- coding: utf-8 -*-

import sys
sys.path.append("../pyUSBtin")
from pyusbtin.usbtin import USBtin
from pyusbtin.canmessage import CANMessage

sys.path.append("../")
from OpenFlowMeter import OpenFlowMeter
from CANsetup import CANsetup
from PlotData import plotVoltageVsDAC, plotCurrentVsDAC, plotResistanceVsDAC

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


def DACsweep(ofm, channel = [0, 1], steps = 128):
    # initialise dictionaries of arrays to store data
    dac = {}
    voltage = {}
    current = {}

    for chan in channel:
        voltage[chan] = np.array([])
        current[chan] = np.array([])
        dac[chan] = np.array([])

    for DAC in np.linspace(start=0, stop=1023, num=steps, endpoint=True).astype(int):
        print("%d "%(DAC), end="", flush=True)
        # set DAC
        DACset = [0, 0]
        for chan in channel:
            dac[chan]= np.append(dac[chan], DAC)
            DACset[chan] = DAC

        if ofm:
            ofm.setDAC(DACset[0], DACset[1])

        # wait some seconds to settle everything
        time.sleep(2)

        # wait until we have a new message
        if ofm:
            while not ofm.hasNewMessage:
                time.sleep(0.5)

        if ofm:
            for chan in channel:
                current[chan] = np.append(current[chan], ofm.current(chan))
                voltage[chan] = np.append(voltage[chan], ofm.voltage(chan))

    # switch off current
    if ofm:
        ofm.setDAC(0, 0)

    print("\n...done")

    return dac, voltage, current

if __name__ == "__main__":
    main()


