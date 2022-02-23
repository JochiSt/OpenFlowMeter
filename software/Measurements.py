# -*- coding: utf-8 -*-
"""

"""

import numpy as np
import time

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

            ofm.hasNewMessage = False

    # switch off current
    if ofm:
        ofm.setDAC(0, 0)

    print("\n...done")

    return dac, voltage, current

def StabilityTest(ofm, channel=[0,1], DACs = [128], repetitions=200):
    # prepare data structures
    voltage = {}
    current = {}

    for chan in channel:
        voltage[chan] = {}
        current[chan] = {}
        for dac in DACs:
            voltage[chan][dac] = np.array([])
            current[chan][dac] = np.array([])

    # set DAC
    for dac in DACs:
        DACset = [dac,dac]
        if ofm:
            ofm.setDAC(DACset[0], DACset[1])

        # wait some seconds to settle everything
        time.sleep(2)

        for rep in range(repetitions):
            # wait until we have a new message
            if ofm:
                while not ofm.hasNewMessage:
                    time.sleep(0.5)

            if ofm:
                for chan in channel:
                    current[chan][dac] = np.append(current[chan][dac], ofm.current(chan))
                    voltage[chan][dac] = np.append(voltage[chan][dac], ofm.voltage(chan))

                ofm.hasNewMessage = False

    if ofm:
        ofm.setDAC(0, 0)

    print("\n...done")
    return voltage, current

def CurrentCalibration(ofm, channel=0, DACs=[], repetitions=10):

    voltage = np.array([])
    current = np.array([])
    MMcurrent = np.array([])

    # set DAC
    for dac in DACs:
        DACset = [dac,dac]
        if ofm:
            ofm.setDAC(DACset[0], DACset[1])

        # wait some seconds to settle everything
        time.sleep(2)

        # read current from MultiMeter
        readCurrent = float(input("read current: "))
        if readCurrent < 0:
            break

        MMcurrent = np.append(MMcurrent, readCurrent)
        for rep in range(repetitions):
            # wait until we have a new message
            if ofm:
                ofm.waitForNewMessage()

            if ofm:
                current = np.append(current, ofm.current(channel))
                voltage = np.append(voltage, ofm.voltage(channel))

                ofm.hasNewMessage = False

    return voltage, current, MMcurrent
