# -*- coding: utf-8 -*-
"""

"""

import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append("../")

import os


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

    ###########################################################
    # plot resistance
    ax3 = ax1.twinx()
    color = 'tab:green'
    ax3.spines['right'].set_position(('outward', 60))
    ax3.set_ylabel('OFM resistance / Ohm', color=color)  # we already handled the x-label with ax1

    resistance = voltage / current

    ax3.plot( dac[3:], resistance[3:], color=color)
    ax3.tick_params(axis='y', labelcolor=color)
    ax3.set_ylim([100*0.9,100*1.1])

    # add vertical line for 1mA which is about 32 LSB
    ax3.vlines(32, 0, 200)

    # get closest index of a value in an array
    def find_nearest_idx(array, value):
        array = np.asarray(array)
        idx = (np.abs(array - value)).argmin()
        return idx

    dac_1mA_idx = find_nearest_idx( dac, 32)
    resistance_1mA = resistance[dac_1mA_idx]
    print("resistance at DAC=",dac[dac_1mA_idx],"LSBs is ", resistance_1mA , " Ohm" )

    print( resistance[dac_1mA_idx-3 : dac_1mA_idx+3] )

    ax3.hlines(resistance_1mA, 0, 1023, color=color, linestyle="--")

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig(os.path.splitext(filename)[0]+".png")
    plt.show()

if __name__ == "__main__":
    plot_sweepDAC("measurement_20220309_065823_CH0_1023.npz")
    #plot_sweepDAC("measurement_20220309_065823_CH1_1023.npz")

    plot_sweepDAC("measurement_20220311_081058_CH0_1023.npz")
    #plot_sweepDAC("measurement_20220311_081058_CH1_1023.npz")
