# -*- coding: utf-8 -*-
"""

"""

import numpy as np

import sys
sys.path.append("../")

import matplotlib.pyplot as plt

def plot_calibration(filename):
    npzfile = np.load(filename)

    voltage = npzfile['voltage']
    current = npzfile['current']            # OpenFlowMeter measured current
    MMcurrent = npzfile['MMcurrent']  # Multimeter measured current

    MMcurrent =np.array(  [0 if v is None else v for v in MMcurrent] )

    voltage *= 3.3/4095
    current *= 3.3/4095 * 10
    MMcurrent /= 10 # to get it in mA

    fig, ax1 = plt.subplots()

    color = 'tab:red'
    ax1.set_xlabel("multimeter current / mA")
    ax1.set_ylabel("OFM current / mA", color=color)
    ax1.plot( MMcurrent, current, color=color, label="calibration", marker="." )
    ax1.plot( [0,30], [0,30], color=color, linestyle='--',label="y=x")
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis

    color = 'tab:blue'
    ax2.set_ylabel('OFM voltage / V', color=color)  # we already handled the x-label with ax1
    ax2.plot( MMcurrent, voltage, color=color)
    ax2.tick_params(axis='y', labelcolor=color)

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

    #return npzfile['dac'], npzfile['current'], npzfile['voltage']

if __name__ == "__main__":
    #plot_calibration("calibration_20220307_133034_CH0_10.npz")
    #plot_calibration("calibration_20220307_190727_CH0_100.npz")
    plot_calibration("calibration_20220308_191237_CH0_10.npz")
