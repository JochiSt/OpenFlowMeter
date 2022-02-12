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
        dac, voltage, current = DACsweep(ofm=ofm, channel=channels, steps = 16)
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

    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    # analyse data
    for chan in channels:
        ax1.plot(dac[chan], voltage[chan],          label="U%d"%chan)
        ax2.plot(dac[chan], current[chan]*1000, label="I%d"%chan)

    ax1.set_xlabel('DAC / LSB')
    ax1.set_ylabel('voltage / V')
    ax2.set_ylabel("current / mA")

    lines, labels    = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax2.legend(lines + lines2, labels + labels2, loc=0)

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

    for DAC in np.linspace(start=0, stop=1023, num=steps, endpoint=True).astype(int):
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

    return dac, voltage, current

if __name__ == "__main__":
    main()


