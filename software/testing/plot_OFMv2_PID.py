# -*- coding: utf-8 -*-

import sys
sys.path.append("../")
from OpenFlowMeter import PT100
from OpenFlowMeter import convertVoltage, convertCurrent

import matplotlib.pyplot as plt
import numpy as np

import time


PLOT_RESISTANCE = False


def plot_OFMv2_PID(filename):
    print('#'*40)
    print(filename)
    npzfile = np.load(filename)

    # OpenFlowMeter measured currents & voltages
    timestamp    = npzfile['timestamp']
    temperatures = [ npzfile['temperature0'], npzfile['temperature1'] ]
    setp         = [ npzfile['setp0'], npzfile['setp1'] ]
    dac          = [ npzfile['dac0'], npzfile['dac1'] ]

    fig, ax = plt.subplots(2, 1, figsize=(6,10))

    # temperatures
    color = 'tab:blue'

    for i in [0,1]:
        #ax[i].plot( timestamp, t_tmp100, label="T TMP100", color='lightsteelblue')
        ax[i].set_ylabel("Temperature / degC", color=color)
        ax[i].tick_params(axis='y', labelcolor=color)

        ax[i].plot( timestamp, setp[i], label="setpoint")
        #ax[i].axhline(ofm.config.PID_T[i])

    """
    for gain in [0,1]:
        colors = ['mediumblue', 'cornflowerblue']
        ax[0].plot( timestamp, PT100.convertPT100_T(r_0[gain]),
                   label="T CH0 gain %d"%(gain), color=colors[gain])
        ax[1].plot( timestamp, PT100.convertPT100_T(r_1[gain]),
                   label="T CH1 gain %d"%(gain), color=colors[gain])
    """

    for i in [0,1]:
        ax[i].plot( timestamp, temperatures[i], label="calc. T", color='deeppink', linewidth=1)

    # DAC setpoint
    ax2 = [
        ax[0].twinx(),
        ax[1].twinx()
        ]

    color = 'tab:orange'
    for i in [0,1]:
        ax2[i].set_ylabel("DAC setpoint / LSB", color=color)
        ax2[i].tick_params(axis='y', labelcolor=color)
        ax2[i].plot( timestamp, dac[i], label="DAC", color=color)

    ax3 = [
        ax[0].twinx(),
        ax[1].twinx()
        ]

    # resistance
    color = 'tab:green'
    for i in [0,1]:
        ax3[i].set_ylabel("resistance / Ohm", color=color)
        ax3[i].spines['right'].set_position(('outward', 60))
        ax3[i].tick_params(axis='y', labelcolor=color)

    """
    if PLOT_RESISTANCE:
        for gain in [0,1]:
            colors = ['forestgreen', 'lime']

            ax3[0].plot( timestamp, r_0[gain], label="R CH0 gain %d"%(gain),
                        color=colors[gain])
            ax3[1].plot( timestamp, r_1[gain], label="R CH1 gain %d"%(gain),
                        color=colors[gain])
    """

    for i in [0,1]:
        ax[i].set_title("OFM PID test / evaluation Channel %d"%(i))
        ax[i].set_xlabel("measurement time / s")
        ax[i].set_xlim([25,75])

    """
    for i in [0,1]:
        ax[i].text(0.2, 0.95, "T %f\nP %f\nI %f\nD %f"%(
                ofm.config.PID_T[i],
                ofm.config.PID_P[i],
                ofm.config.PID_I[i],
                ofm.config.PID_D[i]
            ),
             horizontalalignment='left',
             verticalalignment='top',
             transform=ax[i].transAxes,
             fontfamily = 'monospace',
             fontsize = 'medium')
        #ofm.config.PID_T[1] = 30.0
    """
    #fig.legend()

    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_OFMv2_PID('PIDtest20230107_102652_.npz')


