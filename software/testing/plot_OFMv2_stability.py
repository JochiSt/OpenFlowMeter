# -*- coding: utf-8 -*-

import sys
sys.path.append("../")

import numpy as np
import matplotlib.pyplot as plt

def plot_OFMv2_stability(filename):
    npzfile = np.load(filename)

    dacs = npzfile['dacs']
    voltage0 =  npzfile['voltage0']
    current0 =  npzfile['current0']
    voltage1 =  npzfile['voltage1']
    current1 =  npzfile['current1']

    ###########################################################################
    """
    voltage0 = voltage0 / (3.3/4095) # 1 LSB = 0,8 mV
    voltage1 = voltage1 / (3.3/4095)

    current0 = current0 / (3.3/4095 * 10e-3)*1e3 # 1 LSB = 8 uA
    current1 = current1 / (3.3/4095 * 10e-3)*1e3
    """
    fig, (ax1, ax2) = plt.subplots(1, 2)

    ###########################################################################

    ax1.plot( dacs, voltage1 / voltage0, label="voltage", marker=".", linestyle = "-")
    ax1.plot( dacs, current1 / current0, label="curent", marker=".", linestyle = "-")

    ax1.set_title("voltage & current gain")

    ax1.set_xscale('log', base=2)
    ax1.set_xlim([2**0, 2**10])
    ax1.set_xlabel("DAC setpoint LSB")
    ax1.set_ylabel("gain")
    ax1.legend()


    ###########################################################################

    ax2a = ax2.twinx()
    ax2.set_xscale('log', base=2)
    ax2.set_xlabel("DAC setpoint LSB")

    ax2.plot( dacs, voltage0, label="voltage 0", marker="*", linestyle = "-", color="g")
    ax2.plot( dacs, voltage1, label="voltage 1", marker=".", linestyle = "-", color="g")
    ax2a.plot( dacs, current0, label="current 0", marker="*", linestyle = "-", color="r")
    ax2a.plot( dacs, current1, label="current 1", marker=".", linestyle = "-", color="r")

    ax2.set_title("voltage & current response")

    ax2.set_ylabel("voltage / LSB")
    ax2.set_yscale('log', base=2)

    ax2a.set_ylabel("current / LSB")
    ax2a.set_yscale('log', base=2)

    ax2.legend()

    ax2.set_xlim([2**0, 2**10])

    fig.tight_layout()
    plt.show()

    ###########################################################################

    fig, (ax1) = plt.subplots(1, 1)

    ax1.plot(current0 * 3.3/4095 * 10e-3 * 1e3, voltage0 * 3.3/4095,
             label="gain 0", marker=".", linestyle = "-" )
    ax1.plot(current1 * 3.3/4095 * 10e-3 * 1e3, voltage1 * 3.3/4095,
             label="gain 1", marker=".", linestyle = "-" )
    ax1.legend()

    ax1.set_xlabel("current / mA")
    ax1.set_ylabel("voltage / V")

    fig.tight_layout()
    plt.show()

    ###########################################################################

    fig, (ax1) = plt.subplots(1, 1)

    ax1.plot(voltage0, voltage1,
             label="voltage", marker=".", linestyle = "", color='g' )
    ax1.plot(current0, current1,
             label="current", marker=".", linestyle = "", color='r' )


    ax1.set_xlabel("gain setting 0 / LSB")
    ax1.set_ylabel("gain setting 1 / LSB")
    ax1.set_xlim([0, 1000])

    # fit slope to determine the gain
    data_selection = np.where(voltage1<3000)

    m, b = np.polyfit(voltage0[data_selection], voltage1[data_selection], deg=1)
    ax1.axline(xy1=(0, b), slope=m, label=f'$y = {m:.2f}x {b:+.2f}$', color='g')

    m, b = np.polyfit(current0[data_selection], current1[data_selection], deg=1)
    ax1.axline(xy1=(0, b), slope=m, label=f'$y = {m:.2f}x {b:+.2f}$', color='r')

    ax1.legend()

    fig.tight_layout()
    plt.show()


    ###########################################################################

    fig, (ax1) = plt.subplots(1, 1)
    ax1.plot(dacs, (voltage0 * 3.3/4095) / (current0 * 3.3/4095 * 10e-3),
             label="gain 0", marker=".", linestyle = "-" )
    ax1.plot(dacs, (voltage1 * 3.3/4095) / (current1 * 3.3/4095 * 10e-3),
             label="gain 1", marker=".", linestyle = "-" )
    ax1.legend()

    ax1.set_xlim([2**0, 2**10])
    ax1.set_xscale('log', base=2)
    ax1.set_ylabel("resistance / Ohm")
    ax1.set_xlabel("DAC setting / LSB")

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

if __name__ == "__main__":
    plot_OFMv2_stability("stability_v2_20221216_191453_CH0_100.npz")
    plot_OFMv2_stability("stability_v2_20221216_200204_CH1_100.npz")


