# -*- coding: utf-8 -*-

import sys
sys.path.append("../")
from OpenFlowMeter import OpenFlowMeter_Config

import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np

PLOT_RESISTANCE = False


def plot_OFMv2_PID(filename):
    if not filename:
        return

    print('#'*40)
    print(filename)
    npzfile = np.load(filename)

    # OpenFlowMeter measured currents & voltages
    timestamp    = npzfile['timestamp']
    temperatures = npzfile['temperatures']

    voltages = npzfile['voltages']
    currents = npzfile['currents']

    current_raw = npzfile['current_raw']
    voltage_raw = npzfile['voltage_raw']

    setp         = npzfile['setp']
    dac          = npzfile['dac']

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
        ax2[i].set_ylim([0,4096])
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
        ax5[i].yaxis.set_major_locator(MaxNLocator(integer=True))

        ax5[i].plot(timestamp, np.right_shift(gains, (2*i)) & 0x3,
                    label="gains", color=color, marker='.', linestyle='')

        ax5[i].set_ylim([0,3.1])

    ###########################################################################
    # raw values
    ax6 = [
        ax[0].twinx(),
        ax[1].twinx()
        ]
    color = 'black'
    for i in [0,1]:
        ax6[i].set_ylabel("raw values / LSB", color=color)
        ax6[i].spines['right'].set_position(('outward', 55+55+55+40))
        ax6[i].tick_params(axis='y', labelcolor=color)
        ax6[i].set_yscale('log', base=2)


        for gain in [0,1]:
            ax6[i].plot(timestamp, current_raw[i][gain][:len(timestamp)],
                    label="current G=%d"%(gain), color=color, marker='',
                    linestyle='-', linewidth=1+gain)

            ax6[i].plot(timestamp, voltage_raw[i][gain][:len(timestamp)],
                    label="current G=%d"%(gain), color='gray', marker='',
                    linestyle='-', linewidth=1+gain)
        ax6[i].set_ylim([1,4400])

    ###########################################################################
    # evaluate stable temperature

    # get starting time
    t_start = None
    t_stop  = None

    for (t, event) in events:
        if event == "PID enabled":
            t_start = float(t) + 20
        elif event == "PID disabled":
            t_stop = float(t)
        elif "PID setpoint" in event:
            t_stop = float(t)
            break

    sel_times = np.where( (t_start < timestamp) & ( timestamp < t_stop) )

    for ch in [0,1]:
        print("Temperature", ch)
        print("", np.mean(temperatures[ch][sel_times]), "+-", np.std(temperatures[ch][sel_times]))

    ###########################################################################
    # X axis
    for i in [0,1]:
        ax[i].set_title("OFM PID test / evaluation Channel %d"%(i))
        ax[i].set_xlabel("measurement time / s")

        #ax[i].set_xlim([45,48])

        ax[i].legend(loc='lower right')

    ###########################################################################
    # PID information
    for i in [0,1]:
        ax6[i].text(0.1, 0.95, "T %9.6f\nP %9.6f\nI %9.6f\nD %9.6f"%(
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
    plot_OFMv2_PID('PIDtest_20230227_153203.npz')


