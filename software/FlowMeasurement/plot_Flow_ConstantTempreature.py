# -*- coding: utf-8 -*-

import numpy as np
import matplotlib.pyplot as plt

import sys
sys.path.append("../")

import os


def plot_Flow_ConstantTemperature(filename):
    npzfile = np.load(filename)

    log_dac=npzfile['log_dac'][2:]
    log_time=npzfile['log_time'][2:]
    log_T=npzfile['log_T'][2:]
    log_current=npzfile['log_current'][2:]
    log_voltage=npzfile['log_voltage'][2:]

    fig, ax1 = plt.subplots()
    ax1.set_title("DAC sweep")
    color = 'tab:red'
    ax1.set_xlabel("measurement time / s")
    ax1.set_ylabel("OFM current / LSB", color=color)
    ax1.plot( log_time, log_current, color=color, label="calibration", marker="." )
    #ax1.set_ylim([0,33])
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('OFM voltage / LSB', color=color)  # we already handled the x-label with ax1
    ax2.plot( log_time, log_voltage, color=color)
    ax2.tick_params(axis='y', labelcolor=color)
    #ax2.set_ylim([0,4.0])


    ax3 = ax1.twinx()
    color = 'tab:green'
    ax3.spines['right'].set_position(('outward', 60))
    ax3.set_ylabel('OFM temperature / °C', color=color)  # we already handled the x-label with ax1
    ax3.plot( log_time, log_T, color=color)
    ax3.tick_params(axis='y', labelcolor=color)

    ax4 = ax1.twinx()
    color = 'tab:orange'
    ax4.spines['right'].set_position(('outward', 120))
    ax4.set_ylabel('OFM dac / LSB', color=color)  # we already handled the x-label with ax1
    ax4.plot( log_time, log_dac, color=color)
    ax4.tick_params(axis='y', labelcolor=color)

    """
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
    """
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.savefig(os.path.splitext(filename)[0]+".png")
    plt.show()

if __name__ == "__main__":
    plot_Flow_ConstantTemperature("Tregulation_20220314_070804_CH1_40.npz")