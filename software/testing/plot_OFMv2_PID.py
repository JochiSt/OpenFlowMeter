# -*- coding: utf-8 -*-

import sys
sys.path.append("../")
from OpenFlowMeter import OpenFlowMeter_Config
from OpenFlowMeter import PT100
from OpenFlowMeter import convertVoltage, convertCurrent

import matplotlib.pyplot as plt
import numpy as np

import time


PLOT_RESISTANCE = False


def plot_OFMv2_PID(filename):
    if not filename:
        return

    print('#'*40)
    print(filename)
    npzfile = np.load(filename)

    # OpenFlowMeter measured currents & voltages
    timestamp    = npzfile['timestamp']
    temperatures = [ npzfile['temperature0'], npzfile['temperature1'] ]

    voltages = [ npzfile['voltage0'], npzfile['voltage1'] ]
    currents = [ npzfile['current0'], npzfile['current1'] ]

    setp         = [ npzfile['setp0'], npzfile['setp1'] ]
    dac          = [ npzfile['dac0'], npzfile['dac1'] ]

    events       = npzfile['events']
    ofmcfg       = OpenFlowMeter_Config()
    ofmcfg.fromBytes( npzfile['ofmcfg'] )

    gains        = npzfile['gains'].astype(int)
    # ofmcfg.printout()

    fig, ax = plt.subplots(2, 1, figsize=(8,10))

    ###########################################################################
    # temperatures
    color = 'tab:blue'
    for i in [0,1]:
        #ax[i].plot( timestamp, t_tmp100, label="T TMP100", color='lightsteelblue')
        ax[i].set_ylabel("Temperature / degC", color=color)
        ax[i].tick_params(axis='y', labelcolor=color)

        ax[i].plot( timestamp, setp[i], label="setpoint")

        for (t, event) in events:
            vline_color = next(ax[i]._get_lines.prop_cycler)['color']
            ax[i].axvline(float(t), label=event,
                          color = vline_color, linewidth=1)

    for i in [0,1]:
        ax[i].plot( timestamp, temperatures[i], label="calc. T", color='deeppink', linewidth=1)

    ###########################################################################
    # DAC setpoint
    ax2 = [
        ax[0].twinx(),
        ax[1].twinx()
        ]

    color = 'tab:orange'
    for i in [0,1]:
        ax2[i].set_ylabel("DAC value / LSB", color=color)
        ax2[i].set_ylim([0,1024])
        ax2[i].tick_params(axis='y', labelcolor=color)
        ax2[i].plot( timestamp, dac[i], label="DAC", color=color)

    ###########################################################################
    # current
    ax3 = [
        ax[0].twinx(),
        ax[1].twinx()
        ]
    color = 'tab:green'
    for i in [0,1]:
        ax3[i].set_ylabel("current / mA", color=color)
        ax3[i].spines['right'].set_position(('outward', 55))
        ax3[i].tick_params(axis='y', labelcolor=color)

        ax3[i].plot(timestamp, currents[i]*1000, label="current", color=color)

    ###########################################################################
    # voltage
    ax4 = [
        ax[0].twinx(),
        ax[1].twinx()
        ]
    color = 'tab:olive'
    for i in [0,1]:
        ax4[i].set_ylabel("voltage / V", color=color)
        ax4[i].spines['right'].set_position(('outward', 55+55))
        ax4[i].tick_params(axis='y', labelcolor=color)

        ax4[i].plot(timestamp, voltages[i], label="voltage", color=color)

    ###########################################################################
    # gains
    ax5 = [
        ax[0].twinx(),
        ax[1].twinx()
        ]
    color = 'red'
    for i in [0,1]:
        ax5[i].set_ylabel("gains", color=color)
        ax5[i].spines['right'].set_position(('outward', 55+55+55))
        ax5[i].tick_params(axis='y', labelcolor=color)

        ax5[i].plot(timestamp, np.right_shift(gains, (2*i)) & 0x3,
                    label="gains", color=color, marker='.', linestyle='')

        ax5[i].set_ylim([0,3.1])


    ###########################################################################
    # X axis
    for i in [0,1]:
        ax[i].set_title("OFM PID test / evaluation Channel %d"%(i))
        ax[i].set_xlabel("measurement time / s")

        #ax[i].set_xlim([45,48])

        ax[i].legend()

    ###########################################################################
    # PID information
    for i in [0,1]:
        ax5[i].text(0.1, 0.95, "T %9.6f\nP %9.6f\nI %9.6f\nD %9.6f"%(
                ofmcfg.PID_T[i],
                ofmcfg.PID_P[i],
                ofmcfg.PID_I[i],
                ofmcfg.PID_D[i]
            ),
             horizontalalignment='left',
             verticalalignment='top',
             transform=ax[i].transAxes,
             fontfamily = 'monospace',
             fontsize = 'medium',
             bbox = dict(facecolor='white',
                         ec="0.5",
                         alpha=0.7)
             )

    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_OFMv2_PID('PIDtest20230107_102652_.npz')


