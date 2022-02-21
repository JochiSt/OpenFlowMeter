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

    # plot voltage
    for dac in dac_steps:
        if dac == 0:
            continue
        plt.plot( npzfile['U'+str(dac)], label="DAC = %d"%(dac) )

    plt.legend()
    plt.show()

    # plot current
    for dac in dac_steps:
        if dac == 0:
            continue
        plt.plot( npzfile['I'+str(dac)] * 1000, label="DAC = %d"%(dac) )

    plt.legend()
    plt.show()

    # plot resistance
    for dac in dac_steps:
        if dac == 0:
            continue
        plt.plot( npzfile['U'+str(dac)] / npzfile['I'+str(dac)], label="DAC = %d"%(dac))

    plt.legend()
    plt.show()

    # plot all points
    all_U = np.array([])
    all_I = np.array([])
    for dac in dac_steps:
        if dac == 0:
            continue
        all_U = np.append( all_U, npzfile['U'+str(dac)])
        all_I = np.append( all_I, npzfile['I'+str(dac)])

    plt.plot( all_U, all_I )
    plt.legend()
    plt.show()

    #return npzfile['dac'], npzfile['current'], npzfile['voltage']

if __name__ == "__main__":
    plot_stability("stability_20220220_211134_CH0_1000.npz")
