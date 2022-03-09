# -*- coding: utf-8 -*-
"""

"""

import numpy as np
from scipy.optimize import curve_fit

import sys
sys.path.append("../")

import matplotlib.pyplot as plt

def plot_calibration(filename):
    npzfile = np.load(filename)

    voltage = npzfile['voltage']
    current = npzfile['current']            # OpenFlowMeter measured current
    MMcurrent = npzfile['MMcurrent']  # Multimeter measured current
    dac_setp = npzfile['dac_steps']

    # we have to recover the DAC setting for each measurement point
    # only all DAC settings are given
    repetitions = int( len(voltage)/len(dac_setp) )
    dac_steps = np.array([])
    for dac in dac_setp:
        dac_steps = np.append(dac_steps, np.ones(repetitions)*dac)

    MMcurrent =np.array(  [0 if v is None else v for v in MMcurrent] )

    voltage *= 3.3/4095
    current *= 3.3/4095 * 10    # 10mA = 1V
    MMcurrent /= 10 # to get it in mA

    fig, ax1 = plt.subplots()
    ax1.set_title("OFM current vs. Multimeter current")
    color = 'tab:red'
    ax1.set_xlabel("multimeter current / mA")
    ax1.set_ylabel("OFM current / mA", color=color)
    ax1.plot( MMcurrent, current, color=color, label="calibration", marker="." )
    ax1.plot( [0,33], [0,33], color=color, linestyle='--',label="y=x")
    ax1.set_ylim([0,33])
    ax1.set_xlim([0,max(MMcurrent)])
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('OFM voltage / V', color=color)  # we already handled the x-label with ax1
    ax2.plot( MMcurrent, voltage, color=color)
    ax2.plot( [0,40], [0,4], color=color, linestyle='--',label="y=x")
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim([0,4.0])

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

    fig, ax1 = plt.subplots()
    ax1.set_title("Multimeter current vs. DAC setpoint")
    color = 'tab:red'
    ax1.set_xlabel("DAC setting / LSB")
    ax1.set_ylabel("multimeter current / mA", color=color)
    ax1.plot( dac_steps, MMcurrent, color=color, label="calibration", marker="." )
    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim([0,max(MMcurrent)])
    ax1.set_xlim([0,max(dac_steps)])


    def fit_func(x, a):
        return a*x

    popt, pcov = curve_fit(fit_func, dac_steps, MMcurrent, bounds=([0], [0.05]) )
    perr = np.sqrt(np.diag(pcov))

    print(popt, perr)
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

if __name__ == "__main__":
    #plot_calibration("calibration_20220307_133034_CH0_10.npz")
    #plot_calibration("calibration_20220307_190727_CH0_100.npz")
    #plot_calibration("calibration_20220308_191237_CH0_10.npz")
    plot_calibration("calibration_20220308_194833_CH0_10.npz")
