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

    # plot all points
    all_U = np.array([])
    all_I = np.array([])
    for dac in dac_steps:
        if dac == 0:
            continue
        all_U = np.append( all_U, npzfile['U'+str(dac)])
        all_I = np.append( all_I, npzfile['I'+str(dac)])

    plt.xlabel("voltage / LSB")
    plt.ylabel("current / LSB")
    plt.plot( all_U, all_I,   label="all measurement points", marker=".", linestyle = "")
    plt.legend()
    plt.show()

    fig, ax1 = plt.subplots()
    ax1.set_title("OFM stability")
    # plot voltage
    for dac in dac_steps:
        if dac == 0:
            continue
        ax1.plot( npzfile['U'+str(dac)], label="DAC = %d"%(dac) )

    ax1.set_ylabel("voltage / LSB")
    ax1.set_xlabel("measurement point")
    ax1.legend()

    ax2 = ax1.twinx()

    # plot current
    for dac in dac_steps:
        if dac == 0:
            continue
        ax2.plot( npzfile['I'+str(dac)], label="DAC = %d"%(dac), linestyle="--" )

    ax2.set_ylabel("current / LSB (dotted)")
    ax2.set_ylim( [min(all_I)*0.8, max(all_I)*1.2] )

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

    ###
    # histogramming
    for dac in dac_steps:
        if dac == 0:
            continue
        current = np.array(npzfile['I'+str(dac)])
        n, bins, patches = plt.hist(current , np.linspace(0,1024,512),  label="DAC = %d"%(dac))

    plt.xlabel('OFM measured current / LSB')
    plt.ylabel('#')
   # plt.yscale('log', nonposy='clip')
    plt.title('Histogram of OFM measured current')
    plt.legend()
    plt.show()

    for dac in dac_steps:
        if dac == 0:
            continue
        voltage = np.array(npzfile['U'+str(dac)])
        n, bins, patches = plt.hist(voltage , np.linspace(0,1024,512),  label="DAC = %d"%(dac))

    plt.xlabel('OFM measured voltage / LSB')
    plt.ylabel('#')
    #plt.yscale('log', nonposy='clip')
    plt.title('Histogram of OFM measured voltage')
    plt.legend()
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
    #plot_stability("stability_20220220_211134_CH0_1000.npz")
    #plot_stability("stability_20220220_211134_CH1_1000.npz")

    #plot_stability("stability_20220311_110956_CH0_1000.npz")
    #plot_stability("stability_20220311_115830_CH0_1000.npz")

    plot_stability("stability_20220311_124812_CH1_100.npz")