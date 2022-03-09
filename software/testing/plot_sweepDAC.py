# -*- coding: utf-8 -*-
"""

"""

import numpy as np
from scipy.optimize import curve_fit

import sys
sys.path.append("../")

import matplotlib.pyplot as plt

def plot_sweepDAC(filename):
    npzfile = np.load(filename)

    voltage = npzfile['voltage']
    current = npzfile['current']            # OpenFlowMeter measured current
    dac = npzfile['dac']

    fig, ax1 = plt.subplots()
    ax1.set_title("DAC sweep")
    color = 'tab:red'
    ax1.set_xlabel("DAC / LSB")
    ax1.set_ylabel("OFM current / mA", color=color)
    ax1.plot( dac, current*1000, color=color, label="calibration", marker="." )
    ax1.set_ylim([0,33])
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('OFM voltage / V', color=color)  # we already handled the x-label with ax1
    ax2.plot( dac, voltage, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim([0,4.0])

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

if __name__ == "__main__":
    plot_sweepDAC("measurement_20220309_065823_CH0_1023.npz")
