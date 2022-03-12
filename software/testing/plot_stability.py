# -*- coding: utf-8 -*-
"""

"""

import numpy as np

import sys
sys.path.append("../")

import matplotlib.pyplot as plt

def plot_stability(filename):
    npzfile = np.load(filename)
    dac_steps = npzfile['dac_steps']


    fig, (ax1, ax2) = plt.subplots(1, 2)
    # plot all points
    all_U = np.array([])
    all_I = np.array([])
    for dac in dac_steps:
        if dac == 0:
            continue
        all_U = np.append( all_U, npzfile['U'+str(dac)])
        all_I = np.append( all_I, npzfile['I'+str(dac)])

    ax1.set_xlabel("voltage / LSB")
    ax1.set_ylabel("current / LSB")
    ax1.plot( all_U, all_I,   label="all points", marker=".", linestyle = "")
    ax1.legend()

    ax2.set_title("OFM stability")
    # plot voltage
    for dac in dac_steps:
        if dac == 0:
            continue
        ax2.plot( npzfile['U'+str(dac)], label="DAC = %d"%(dac) )

    ax2.set_ylabel("voltage / LSB")
    ax2.set_xlabel("measurement point")
    ax2.legend()

    ax2a = ax2.twinx()

    # plot current
    for dac in dac_steps:
        if dac == 0:
            continue
        ax2a.plot( npzfile['I'+str(dac)], label="DAC = %d"%(dac), linestyle="--" )

    ax2a.set_ylabel("current / LSB (dotted)")
    ax2a.set_ylim( [min(all_I)*0.9, max(all_I)*1.1] )

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

    ###
    # histogramming
    fig, (ax1, ax2) = plt.subplots(1, 2)

    for dac in dac_steps:
        if dac == 0:
            continue
        current = np.array(npzfile['I'+str(dac)])
        n, bins, patches = ax1.hist(current , np.linspace(0,1024,128),  label="DAC = %d"%(dac))

    ax1.set_xlabel('OFM measured current / LSB')
    ax1.set_ylabel('#')
   # plt.yscale('log', nonposy='clip')
    ax1.set_title('Current')
    ax1.legend()

    for dac in dac_steps:
        if dac == 0:
            continue
        voltage = np.array(npzfile['U'+str(dac)])
        n, bins, patches = ax2.hist(voltage , np.linspace(0,1024,128),  label="DAC = %d"%(dac))

    ax2.set_xlabel('OFM measured voltage / LSB')
    ax2.set_ylabel('#')
    #plt.yscale('log', nonposy='clip')
    ax2.set_title('Voltage')
    ax2.legend()
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()


    # plot resistance
    for dac in dac_steps:
        if dac == 0:
            continue
        plt.plot( npzfile['U'+str(dac)] / (npzfile['I'+str(dac)] * 10e-3), label="DAC = %d"%(dac))

    plt.title("OFM measured resistance")
    plt.ylabel("resistance / Ohm")
    plt.xlabel("measurement point")
    plt.legend()
    plt.show()

if __name__ == "__main__":
    #plot_stability("stability_20220311_124812_CH0_100.npz")
    #plot_stability("stability_20220311_124812_CH1_100.npz")

    #plot_stability("stability_20220311_221412_CH0_10000.npz")
    plot_stability("stability_20220312_064753_CH1_100.npz")

