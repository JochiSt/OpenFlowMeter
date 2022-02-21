# -*- coding: utf-8 -*-

import sys
sys.path.append("../")
from OpenFlowMeter import OpenFlowMeter
from CANsetup import CANsetup
from Measurements import CurrentCalibration

import time

import numpy as np

def main():
    # initialise USBtin
    setup = CANsetup()

    # initialise OFM
    ofm =  OpenFlowMeter(usbtin = setup.usbtin, boardID=0x1)

    measurement_successful = False

    # configuration
    channel = 0            # channels, we want to analyse
    repetitions = 10      # repeat how many times

    dac_steps = [0, 128, 256, 512, 1023]


    # just for testing python
#    repetitions = 1
#    dac_steps = [128]

    try:
        voltage, current, MMcurrent = CurrentCalibration(ofm=ofm, channel=channel, repetitions = repetitions, DACs = dac_steps)
        measurement_successful = True
    except Exception as e:
        print(e)
        pass

    setup.deinit()

    if not measurement_successful:
        print("Measurement has not been successuful!")
        return

    # save recorded data in NPZ files
    np.savez("calibration_%s_CH%d_%d.npz"%(time.strftime("%Y%m%d_%H%M%S"), channel, repetitions),
                        voltage=voltage, current=current, MMcurrent=MMcurrent, dac_steps=dac_steps)

if __name__ == "__main__":
    main()


