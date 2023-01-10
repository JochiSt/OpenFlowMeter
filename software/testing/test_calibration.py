# -*- coding: utf-8 -*-

import sys
sys.path.append("../")
from OpenFlowMeter import OpenFlowMeter
from CANsetup import CANsetup
from Measurements import CurrentCalibration
from DMMsetup import DMMsetup

from plot_OFMv2_calibration import plot_calibration

import time

import numpy as np

def test_calibration():
    dmmsetup = None
    cansetup = None

    filename = None

    print("Starting time:", time.strftime("%Y%m%d_%H%M%S") )

    try:
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
        dac_steps = np.linspace(0, 128, 129).astype(int)
        dac_steps = np.append(dac_steps, np.linspace(128, 1024, 100).astype(int))

        # just for testing python
    #    repetitions = 1
    #    dac_steps = [128]

        try:
            voltage, current, MMcurrent = CurrentCalibration(ofm=ofm, dmm=dmm, channel=channel, repetitions = repetitions, DACs = dac_steps)
            measurement_successful = True
        except Exception as e:
            print(e)
            pass

        if not measurement_successful:
            print("Measurement has not been successuful!")
            return

        # save recorded data in NPZ files
        filename = "calibration_%s_CH%d_%d.npz"%(time.strftime("%Y%m%d_%H%M%S"), channel, repetitions)
        np.savez(filename,
                    voltage0=voltage[0], current0=current[0],
                    voltage1=voltage[1], current1=current[1],
                    MMcurrent=MMcurrent, dac_steps=dac_steps)
    except Exception as e:
        print(e)
        pass
    finally:
        # deinit all SETUPs
        if dmmsetup:
            dmmsetup.deinit()
        if cansetup:
            cansetup.deinit()

    return filename

if __name__ == "__main__":
    filename = test_calibration()
    if filename:
        print(filename)

        plot_calibration(filename)


