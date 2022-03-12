# -*- coding: utf-8 -*-

import sys
sys.path.append("../")
from OpenFlowMeter import OpenFlowMeter

from CANsetup import CANsetup
from Measurements import StabilityTest

import time

import numpy as np

def main():
    # initialise USBtin
    setup = CANsetup()

    # initialise OFM
    ofm =  OpenFlowMeter(usbtin = setup.usbtin, boardID=0x1)

    measurement_successful = False

    # configuration
    channels = [0,1]            # channels, we want to analyse
    repetitions = 100          # repeat how many times

    dac_steps = [32, 512, 768] #, 64, 96, 128]


    # just for testing python
#    repetitions = 1
#    dac_steps = [128]

    try:
        voltage, current = StabilityTest(ofm=ofm, channel=channels, repetitions = repetitions, DACs = dac_steps)
        measurement_successful = True
    except Exception as e:
        print(e)
        pass

    setup.deinit()

    if not measurement_successful:
        print("Measurement has not been successuful!")
        return

    # convert from ADC LSB into SI
    """
    for chan in channels:
        for dac_step in voltage[chan].keys():
            voltage[chan][dac_step] = 3.3/4095 * voltage[chan][dac_step]
            current[chan][dac_step] = 3.3/4095 * current[chan][dac_step] * 10e-3    # from simulation 1V = 10mA
    """
    # replace keys to be unique
    for chan in channels:
        for k in list(voltage[chan].keys()):
            if type(k) is int:
                # prevent double conversion, because after conversion, the type is str
                voltage[chan]['U'+str(k)] = voltage[chan].pop(k)
                current[chan]['I'+str(k)] = current[chan].pop(k)

    # save recorded data in NPZ files
    for chan in channels:
        np.savez("stability_%s_CH%d_%d.npz"%(time.strftime("%Y%m%d_%H%M%S"), chan, repetitions),
                        **voltage[chan], **current[chan], dac_steps=dac_steps)

if __name__ == "__main__":
    main()


