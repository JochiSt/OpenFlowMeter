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

    gains        = npzfile['gains']
    # ofmcfg.printout()

    fig, ax = plt.subplots(2, 1, figsize=(8,10))

    # temperatures
    color = 'tab:blue'

    for i in [0,1]:
        #ax[i].plot( timestamp, t_tmp100, label="T TMP100", color='lightsteelblue')
        ax[i].set_ylabel("Temperature / degC", color=color)
        ax[i].tick_params(axis='y', labelcolor=color)

        ax[i].plot( timestamp, setp[i], label="setpoint")
        #ax[i].axhline(ofm.config.PID_T[i])

        for (t, event) in events:
            vline_color = next(ax[i]._get_lines.prop_cycler)['color']
            ax[i].axvline(float(t), label=event,
                          color = vline_color, linewidth=1)

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
        ax2[i].set_ylim([0,1024])
        ax2[i].tick_params(axis='y', labelcolor=color)
        ax2[i].plot( timestamp, dac[i], label="DAC", color=color)

    ax3 = [
        ax[0].twinx(),
        ax[1].twinx()
        ]
    # current
    color = 'tab:green'
    for i in [0,1]:
        ax3[i].set_ylabel("current / mA", color=color)
        ax3[i].spines['right'].set_position(('outward', 55))
        ax3[i].tick_params(axis='y', labelcolor=color)

        ax3[i].plot(timestamp, currents[i]*1000, label="current", color=color)

    ax4 = [
        ax[0].twinx(),
        ax[1].twinx()
        ]
    # voltage
    color = 'tab:blue'
    for i in [0,1]:
        ax4[i].set_ylabel("voltage / V", color=color)
        ax4[i].spines['right'].set_position(('outward', 55+55))
        ax4[i].tick_params(axis='y', labelcolor=color)

        ax4[i].plot(timestamp, voltages[i], label="voltage", color=color)


    for i in [0,1]:
        ax[i].set_title("OFM PID test / evaluation Channel %d"%(i))
        ax[i].set_xlabel("measurement time / s")
        ax[i].set_xlim([25,75])

    for i in [0,1]:
        ax[i].text(0.1, 0.95, "T %f\nP %f\nI %f\nD %f"%(
                ofmcfg.PID_T[i],
                ofmcfg.PID_P[i],
                ofmcfg.PID_I[i],
                ofmcfg.PID_D[i]
            ),
             horizontalalignment='left',
             verticalalignment='top',
             transform=ax[i].transAxes,
             fontfamily = 'monospace',
             fontsize = 'medium')

    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    plot_OFMv2_PID('PIDtest20230107_102652_.npz')


