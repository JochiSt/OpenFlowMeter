# -*- coding: utf-8 -*-

import sys
sys.path.append("../")
from OpenFlowMeter import OpenFlowMeter
from CANsetup import CANsetup
from Measurements import CurrentCalibration
from DMMsetup import DMMsetup

import time

import numpy as np
def main():
    # initialise USBtin
    cansetup = CANsetup()
    # initialise DMM
    dmmsetup = DMMsetup()
    dmm = dmmsetup.dmm

    # initialise OFM
    ofm =  OpenFlowMeter(usbtin = cansetup.usbtin, boardID=0x1)
    measurement_successful = False

    # configuration
    channel = 0            # channels, we want to analyse
    repetitions = 10      # repeat how many times
    dac_steps = np.linspace(0,1024, 100).astype(int)

    # just for testing python
#    repetitions = 1
#    dac_steps = [128]

    try:
        voltage, current, MMcurrent = CurrentCalibration(ofm=ofm, dmm=dmm, channel=channel, repetitions = repetitions, DACs = dac_steps)
        measurement_successful = True
    except Exception as e:
        print(e)
        pass

    # deinit all SETUPs
    dmmsetup.deinit()
    cansetup.deinit()

    if not measurement_successful:
        print("Measurement has not been successuful!")
        return

    # save recorded data in NPZ files
    np.savez("calibration_%s_CH%d_%d.npz"%(time.strftime("%Y%m%d_%H%M%S"), channel, repetitions),
                        voltage=voltage, current=current, MMcurrent=MMcurrent, dac_steps=dac_steps)

if __name__ == "__main__":
    main()


