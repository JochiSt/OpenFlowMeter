# -*- coding: utf-8 -*-

import sys
sys.path.append("../pyUSBtin")
from pyusbtin.usbtin import USBtin
from pyusbtin.canmessage import CANMessage

sys.path.append("../")
from OpenFlowMeter import OpenFlowMeter
from CANsetup import CANsetup

import time

import numpy as np
import matplotlib.pyplot as plt

def main():
    # initialise USBtin
    setup = CANsetup()

    # initialise OFM
    ofm =  OpenFlowMeter(usbtin = setup.usbtin, boardID=0x1)

    measurement_successful = False

    channels = [0,1]    # channels, we want to analyse

    try:
        dac, voltage, current = DACsweep(ofm=ofm, channel=channels, steps = 256)
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
        current[chan] = 3.3/4095 * current[chan]

    # analyse data
    for chan in channels:
        plt.plot(dac[chan], voltage[chan], label="U%d"%chan)
        plt.plot(dac[chan], current[chan], label="I%d"%chan)

    plt.ylabel('ADC / V')
    plt.xlabel('DAC / LSB')
    plt.legend()
    plt.show()

    resistance = {}
    for chan in channels:
        resistance[chan] = voltage[chan] / current [chan]

    for chan in channels:
        plt.plot(dac[chan][1:], resistance[chan][1:], label="R%d"%chan)

    plt.ylabel('R / LSB')
    plt.xlabel('DAC / LSB')
    plt.legend()
    plt.show()

def DACsweep(ofm, channel = [0, 1], steps = 128):
    # initialise dictionaries of arrays to store data
    dac = {}
    voltage = {}
    current = {}

    for chan in channel:
        voltage[chan] = np.array([])
        current[chan] = np.array([])
        dac[chan] = np.array([])

    for DAC in range(0, 1024, steps):
        # set DAC
        DACset = [0, 0]
        for chan in channel:
            dac[chan]= np.append(dac[chan], DAC)
            DACset[chan] = DAC

        if ofm:
            ofm.setDAC(DACset[0], DACset[1])

        # wait 5 seconds to settle everything
        time.sleep(5)

        # wait until we have a new message
        if ofm:
            while not ofm.hasNewMessage:
                time.sleep(0.5)

        if ofm:
            for chan in channel:
                current[chan] = np.append(current[chan], ofm.current(chan))
                voltage[chan] = np.append(voltage[chan], ofm.voltage(chan))

    # switch off current
    for chan in channel:
        if ofm:
            ofm.setDAC(chan, 0)
            time.sleep(1)

    return dac, voltage, current

if __name__ == "__main__":
    main()


