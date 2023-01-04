# -*- coding: utf-8 -*-
"""

"""

import numpy as np
from scipy.optimize import curve_fit

import sys
sys.path.append("../")
from OpenFlowMeter import convertVoltage, convertCurrent

import matplotlib.pyplot as plt

def plot_calibration(filename):
    npzfile = np.load(filename)

    voltage = [ npzfile['voltage0'], npzfile['voltage1'] ]
    current = [ npzfile['current0'], npzfile['current1'] ]            # OpenFlowMeter measured current

    MMcurrent = npzfile['MMcurrent']  # Multimeter measured current
    dac_setp = npzfile['dac_steps']

    for gain in [0,1]:
        print( len(voltage[gain]), len(current[gain]) )

    print(len(MMcurrent), len(dac_setp))

    # we have to recover the DAC setting for each measurement point
    # only all DAC settings are given
    repetitions = int( len(voltage[0])/len(dac_setp) )
    dac_steps = np.array([])
    for dac in dac_setp:
        dac_steps = np.append(dac_steps, np.ones(repetitions)*dac)

    print(len(dac_steps))

    MMcurrent =np.array(  [0 if v is None else v for v in MMcurrent] )

    for gain in [0,1]:
        voltage[gain] = convertVoltage( voltage[gain], gain )
        current[gain] = convertCurrent( current[gain], gain ) *1e3

    MMcurrent /= 10 # to get it in mA

    fig, ax1 = plt.subplots()
    ax1.set_title("OFM current vs. Multimeter current")
    color = 'tab:red'
    ax1.set_xlabel("multimeter current / mA")
    ax1.set_ylabel("OFM current / mA", color=color)
    for gain in [0,1]:
        ax1.plot( MMcurrent, current[gain], color=color, label="calibration", marker="" )

    ax1.plot( [0,33], [0,33], color=color, linestyle='--',label="y=x")
    ax1.set_ylim([0,33])
    ax1.set_xlim([0,max(MMcurrent)])
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx()  # instantiate a second axes that shares the same x-axis
    color = 'tab:blue'
    ax2.set_ylabel('OFM voltage / V', color=color)  # we already handled the x-label with ax1
    for gain in [0,1]:
        ax2.plot( MMcurrent, voltage[gain], color=color)
    ax2.plot( [0,40], [0,4], color=color, linestyle='--',label="y=x")
    ax2.tick_params(axis='y', labelcolor=color)
    ax2.set_ylim([0,4.0])

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

    ###########################################################################
    # FIT MM current and dac steps
    def fit_func(x, a):
        return a*x

    print("Fitting DAC step and MM current")
    popt, pcov = curve_fit(fit_func, dac_steps, MMcurrent, bounds=([0, 0.05]) )
    perr = np.sqrt(np.diag(pcov))
    print("MMcurrent = (", popt[0], "+-", perr[0], ") * dac_step")

    dac_for_1mA = int( 1 / popt[0] )
    print("\t1mA is equal to a DAC setting of %d (0x%X)"%(dac_for_1mA,dac_for_1mA))

    fig, ax1 = plt.subplots()
    ax1.set_title("Multimeter current vs. DAC setpoint")
    color = 'tab:red'
    ax1.set_xlabel("DAC setting / LSB")
    ax1.set_ylabel("multimeter current / mA", color=color)
    ax1.plot( dac_steps, MMcurrent, color=color, label="multimeter current", marker="." )
    ax1.plot( dac_steps, fit_func(dac_steps, popt[0]),
                 label="fit -> 1mA = %d (0x%X) LSB"%(dac_for_1mA,dac_for_1mA))

    ax1.plot( [0, dac_for_1mA ], [1, 1], color='black')
    ax1.plot( [dac_for_1mA, dac_for_1mA ], [0, 1], color='black')

    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim([0,max(MMcurrent)])
    ax1.set_xlim([0,max(dac_steps)])
    ax1.legend()
    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()



    ###########################################################################
    # Fit the HIGH gain section (without saturation)
    HIGH_GAIN_SATURATION = 3.3
    x2 = MMcurrent[MMcurrent  <= HIGH_GAIN_SATURATION]
    y2 = current[1][MMcurrent <= HIGH_GAIN_SATURATION]
    popt, pcov = curve_fit(fit_func, x2, y2, bounds=([0.3, 10]) )
    perr = np.sqrt(np.diag(pcov))
    print("OFM current = (", popt[0], "+-", perr[0], ") * MM current")

    fig, ax3 = plt.subplots()
    ax3.plot( x2, fit_func(x2, popt[0]),
             label="fit high gain (y = %4.3f*x)"%(popt[0]),
             color='green',
             linewidth=6, alpha=0.6)
    ax3.plot( [0,40], [0,40], color='red', linestyle='--',label="y=x")
    ax3.axvline(HIGH_GAIN_SATURATION, color='black', linewidth=0.4)
    ax3.plot(MMcurrent, current[0], marker='.',
             label="current low gain", color='black', alpha=0.2)
    ax3.plot(MMcurrent, current[1], marker='.',
             label="current high gain", color='blue')

    ax3.set_xlim([0,5])
    ax3.set_ylim([0,5])

    ax3.set_ylabel("OFM current / mA")
    ax3.set_xlabel("MM current / mA")

    ax3.set_title("High gain calibration check")

    ax3.legend()

    plt.show()

    ###########################################################################

    fig, ax4 = plt.subplots()
    ax4.plot( MMcurrent, current[1]-fit_func(MMcurrent, popt[0]),
             label="fit high gain (y = %4.3f*x)"%(popt[0]),
             color='green',)
    #        linewidth=6, alpha=0.6)
    #ax5.plot( [0,40], [0,40], color='red', linestyle='--',label="y=x")
    ax4.axvline(HIGH_GAIN_SATURATION, color='black', linewidth=0.4)
    ax4.axhline(0, color='black')
    #ax5.plot(MMcurrent, current[0], marker='.',
    #         label="current low gain", color='black', alpha=0.2)
    #ax5.plot(MMcurrent, current[1], marker='.',
    #         label="current high gain", color='blue')

    ax4.set_xlim([0,3.5])
    ax4.set_ylim([-0.02,0.02])

    ax3.set_ylabel("residual to fit / mA")
    ax4.set_xlabel("MM current / mA")
    ax4.set_title("High gain residuals")
    ax4.legend()
    plt.show()


    ###########################################################################
    # Fit the LOW gain section
    x2 = MMcurrent[MMcurrent  >= HIGH_GAIN_SATURATION]
    y2 = current[0][MMcurrent >= HIGH_GAIN_SATURATION]

    print("Fitting OFM current and MM current")
    popt, pcov = curve_fit(fit_func, x2, y2, bounds=([0.3, 1.2]) )
    perr = np.sqrt(np.diag(pcov))
    print("OFM current = (", popt[0], "+-", perr[0], ") * MM current")

    fig, ax5 = plt.subplots()
    ax5.plot( MMcurrent, current[0]-fit_func(MMcurrent, popt[0]),
             label="fit high gain (y = %4.3f*x)"%(popt[0]),
             color='green',)
    #        linewidth=6, alpha=0.6)
    #ax5.plot( [0,40], [0,40], color='red', linestyle='--',label="y=x")
    ax5.axvline(HIGH_GAIN_SATURATION, color='black', linewidth=0.4)
    #ax5.plot(MMcurrent, current[0], marker='.',
    #         label="current low gain", color='black', alpha=0.2)
    #ax5.plot(MMcurrent, current[1], marker='.',
    #         label="current high gain", color='blue')

    ax5.set_xlim([3.2,30])
    ax5.set_ylim([-0.5,0.5])

    #ax3.set_ylabel("OFM current / mA")
    ax5.set_xlabel("MM current / mA")
    ax5.set_title("Low gain residuals")
    ax5.legend()
    plt.show()

if __name__ == "__main__":

    #plot_calibration("calibration_20230104_085105_CH0_10.npz")
    plot_calibration("calibration_20230104_094358_CH0_10.npz")
