# -*- coding: utf-8 -*-
"""

"""

import numpy as np

import sys
sys.path.append("../")
import PlotData


def readFile(filename):
    npzfile = np.load(filename)
    return npzfile['dac'], npzfile['current'], npzfile['voltage']

if __name__ == "__main__":
    dac, current, voltage = readFile("measurement_CH0_20220213_132416.npz")

    print( voltage[0] )

    PlotData.plotResistanceVsDAC(dac, voltage, current)
