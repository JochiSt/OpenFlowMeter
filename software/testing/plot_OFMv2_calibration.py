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
    print('#'*40)
    print(filename)
    npzfile = np.load(filename)

    # OpenFlowMeter measured currents & voltages
    voltage = [ npzfile['voltage0'], npzfile['voltage1'] ]
    current = [ npzfile['current0'], npzfile['current1'] ]

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

    ###########################################################################
    # check raw values
    print("Saturation / maximum of the raw values (LSB):")
    for gain in [0,1]:
        print("GAIN ", gain)
        print("\tcurrent", np.max( current[gain] ) )
        print("\tvoltage", np.max( voltage[gain] ) )

    ###########################################################################
    # convert LSB into physical values
    for gain in [0,1]:
        voltage[gain] = convertVoltage( voltage[gain], gain )
        current[gain] = convertCurrent( current[gain], gain ) *1e3

    MMcurrent /= 10 # to get it in mA

    ###########################################################################

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
    fig, ax1a = plt.subplots(2, 2, figsize=(6,10))

    ax1a = ax1a.reshape( (4,) )

    ax1a[0].plot(MMcurrent, current[0], marker='')
    ax1a[0].set_xlabel("MM current / mA")
    ax1a[0].set_ylabel("LG current / mA")
    ax1a[0].plot([0,50], [0,50])
    ax1a[0].set_ylim([0,30])
    ax1a[0].set_xlim([0,30])

    ax1a[1].plot(MMcurrent, MMcurrent-current[0], marker='', label='difference to multimeter')
    ax1a[1].set_xlabel("MM current / mA")
    ax1a[1].set_ylabel("MM - LG current / mA")
    ax1a[1].axhline(0)
    #ax1a[1].set_ylim([-0.15, 0.15])
    #ax1a[1].set_xlim([0,3.5])

    ax1a[2].plot(MMcurrent, current[1], marker='')
    ax1a[2].set_xlabel("MM current / mA")
    ax1a[2].set_ylabel("HG current / mA")
    ax1a[2].plot([0,5], [0,5])
    ax1a[2].set_ylim([0,3.5])
    ax1a[2].set_xlim([0,3.5])

    ax1a[3].plot(MMcurrent, MMcurrent-current[1], marker='', label='difference to multimeter')
    ax1a[3].set_xlabel("MM current / mA")
    ax1a[3].set_ylabel("MM - HG current / mA")
    ax1a[3].axhline(0)
    ax1a[3].set_ylim([-0.2,0.2])
    ax1a[3].set_xlim([0,3.5])


    I_MM_LG = MMcurrent-current[0]
    selection = MMcurrent > 2
    selection2 = MMcurrent < 25
    selection = selection & selection2
    I_MM_LG = I_MM_LG[ selection ]
    I_MM_LG = np.mean(I_MM_LG)
    ax1a[1].axhline(I_MM_LG, color='red')
    print("Offset LG", I_MM_LG)

    ax1a[0].plot(MMcurrent[selection], current[0][selection]+I_MM_LG, marker='')
    ax1a[1].plot(MMcurrent[selection],
                 MMcurrent[selection] - (current[0][selection] + I_MM_LG), marker='',
                 label='difference corrected (%5.4f)'%(I_MM_LG))

    I_MM_HG = MMcurrent-current[1]
    selection = MMcurrent > 0.5
    selection2 = MMcurrent < 3
    selection = selection & selection2
    I_MM_HG = I_MM_HG[ selection ]
    I_MM_HG = np.mean(I_MM_HG)
    ax1a[3].axhline(I_MM_HG, color='red')
    print("Offset HG", I_MM_HG)

    ax1a[2].plot(MMcurrent[selection], current[1][selection]+I_MM_HG, marker='')
    ax1a[3].plot(MMcurrent[selection],
                 MMcurrent[selection] - (current[1][selection] + I_MM_HG), marker='',
                 label='difference corrected (%5.4f)'%(I_MM_HG))

    ax1a[1].legend()
    ax1a[3].legend()

    fig.tight_layout()
    plt.show()

    #sys.exit(0)

    ###########################################################################
    # FIT MM current and dac steps
    def fit_func(x, a, b=0):
        return a*x + b

    print("Fitting DAC step and MM current")
    popt, pcov = curve_fit(fit_func, dac_steps, MMcurrent, bounds=([-10, 0.05]) )
    perr = np.sqrt(np.diag(pcov))
    print("MMcurrent = (", popt[0], "+-", perr[0], ") * dac_step")
    print("\tOFFSET: (", popt[1], "+-", perr[1], ")")

    dac_for_1mA = int( 1 / popt[0] )
    print("\t1mA is equal to a DAC setting of %d (0x%X)"%(dac_for_1mA,dac_for_1mA))

    fig, ax1 = plt.subplots()
    ax1.set_title("Multimeter current vs. DAC setpoint")
    color = 'tab:red'
    ax1.set_xlabel("DAC setting / LSB")
    ax1.set_ylabel("multimeter current / mA", color=color)
    ax1.plot( dac_steps, MMcurrent, color=color, label="multimeter current", marker="." )
    ax1.plot( dac_steps, fit_func(dac_steps, popt[0], popt[1]),
                 label="fit -> 1mA = %d (0x%X) LSB"%(dac_for_1mA,dac_for_1mA))

    ax1.plot( [0, dac_for_1mA ], [1, 1], color='black')
    ax1.plot( [dac_for_1mA, dac_for_1mA ], [0, 1], color='black')

    ax1.tick_params(axis='y', labelcolor=color)
    ax1.set_ylim([0,max(MMcurrent)])
    ax1.set_xlim([0,max(dac_steps)])
    ax1.legend()

    fig.tight_layout()  # otherwise the right y-label is slightly clipped
    plt.show()

    print(np.max( current[1] ) )

    ###########################################################################
    # Fit the HIGH gain section (without saturation)
    HIGH_GAIN_SATURATION = convertCurrent( 3900, 1 ) *1e3

    x2 = MMcurrent[MMcurrent  <= HIGH_GAIN_SATURATION]
    y2 = current[1][MMcurrent <= HIGH_GAIN_SATURATION]
    popt, pcov = curve_fit(fit_func, x2, y2, bounds=([-10.0, 10]) )
    perr = np.sqrt(np.diag(pcov))
    print("OFM current = (", popt[0], "+-", perr[0], ") * MM current +",
                          "(", popt[1], "+-", perr[1], ")")

    fig, ax3 = plt.subplots()
    ax3.plot( x2, fit_func(x2, popt[0], popt[1]),
             label="fit high gain (y = %4.3f*x + %4.3f)"%(popt[0], popt[1]),
             color='green',
             linewidth=6, alpha=0.6)

    ax3.plot( [0,40], [0,40], color='red', linestyle='--',label="y=x")

    ax3.axvline(HIGH_GAIN_SATURATION, color='red', linewidth=0.4)
    ax3.axhline(HIGH_GAIN_SATURATION, color='red', linewidth=0.4)

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

    fig.tight_layout()
    plt.show()

    ###########################################################################

    fig, ax4 = plt.subplots()
    ax4.plot( MMcurrent, current[1]-fit_func(MMcurrent, popt[0], popt[1]),
             label="fit residuals high gain (y = %4.3f*x + %4.3f)"%(popt[0], popt[1]),
             color='green',)
    #        linewidth=6, alpha=0.6)
    #ax5.plot( [0,40], [0,40], color='red', linestyle='--',label="y=x")
    ax4.axvline(HIGH_GAIN_SATURATION, color='red', linewidth=0.4)
    ax4.axhline(0, color='black')

    #ax5.plot(MMcurrent, current[0], marker='.',
    #         label="current low gain", color='black', alpha=0.2)
    #ax5.plot(MMcurrent, current[1], marker='.',
    #         label="current high gain", color='blue')

    ax4.set_xlim([0,3.5])
    ax4.set_ylim([-0.02,0.02])

    ax4.set_ylabel("residuals (OFM current - fit) / mA")
    ax4.set_xlabel("MM current / mA")
    ax4.set_title("High gain residuals")
    ax4.legend()

    fig.tight_layout()
    plt.show()

    ###########################################################################
    # Fit the LOW gain section
    x2 = MMcurrent[MMcurrent  >= HIGH_GAIN_SATURATION]
    y2 = current[0][MMcurrent >= HIGH_GAIN_SATURATION]

    print("Fitting OFM current and MM current")
    popt, pcov = curve_fit(fit_func, x2, y2, bounds=([-10.0, 1.2]) )
    perr = np.sqrt(np.diag(pcov))
    print("OFM current = (", popt[0], "+-", perr[0], ") * MM current +",
                          "(", popt[1], "+-", perr[1], ")")

    fig, ax5 = plt.subplots()
    ax5.plot( MMcurrent, current[0]-fit_func(MMcurrent, popt[0], popt[1]),
             label="fit high gain (y = %4.3f*x + %4.3f)"%(popt[0], popt[1]),
             color='green',)
    #        linewidth=6, alpha=0.6)
    #ax5.plot( [0,40], [0,40], color='red', linestyle='--',label="y=x")
    ax5.axvline(HIGH_GAIN_SATURATION, color='red', linewidth=0.4)
    #ax5.plot(MMcurrent, current[0], marker='.',
    #         label="current low gain", color='black', alpha=0.2)
    #ax5.plot(MMcurrent, current[1], marker='.',
    #         label="current high gain", color='blue')

    ax5.set_xlim([0,30])
    ax5.set_ylim([-0.05,0.05])

    ax5.set_ylabel("residuals (OFM current - fit) / mA")
    ax5.set_xlabel("MM current / mA")
    ax5.set_title("Low gain residuals")
    ax5.legend()

    fig.tight_layout()
    plt.show()


    ###########################################################################
    # plot voltages
    x2 =  MMcurrent[MMcurrent  <= HIGH_GAIN_SATURATION]
    y2 = voltage[1][MMcurrent <= HIGH_GAIN_SATURATION]
    popt, pcov = curve_fit(fit_func, x2*1e-3, y2, bounds=([-10.0, 200]) )
    perr = np.sqrt(np.diag(pcov))
    print("HIGH GAIN OFM voltage = (", popt[0], "+-", perr[0], ") * MM current +",
                          "(", popt[1], "+-", perr[1], ")")
    HGohm = popt[0]

    popt, pcov = curve_fit(fit_func, MMcurrent*1e-3, voltage[0], bounds=([-10, 200]) )
    perr = np.sqrt(np.diag(pcov))
    print("LOW gain OFM voltage = (", popt[0], "+-", perr[0], ") * MM current +",
                          "(", popt[1], "+-", perr[1], ")")
    LGohm = popt[0]

    fig, ax6 = plt.subplots()
    #ax6.plot( x2, fit_func(x2, popt[0]),
    #         label="fit high gain (y = %4.3f*x)"%(popt[0]),
    #         color='green',
    #         linewidth=6, alpha=0.6)
    ax6.plot( [0,40], [0,40e-3*LGohm], color='red', linestyle='--',label="LG %5.2f Ohm"%(LGohm))
    ax6.plot( [0,40], [0,40e-3*HGohm], color='green', linestyle='--',label="HG %5.2f Ohm"%(HGohm))

    ax6.axvline(HIGH_GAIN_SATURATION, color='red', linewidth=0.4)
    ax6.plot(MMcurrent, voltage[0], marker='.',
             label="voltage low gain", color='black', alpha=0.2)
    ax6.plot(MMcurrent, voltage[1], marker='.',
             label="voltage high gain", color='blue')

    ax6.set_xlim([0,30])
    ax6.set_ylim([0,3.5])

    ax6.set_ylabel("OFM voltage / V")
    ax6.set_xlabel("MM current / mA")
    ax6.set_title("High gain calibration check")

    ax6.legend()

    fig.tight_layout()
    plt.show()

    ###########################################################################
    # plot the resistance

    fig, ax6 = plt.subplots()

    mmsel = MMcurrent[current[0] > 0]
    vsel = voltage[0][current[0] > 0]
    isel = current[0][current[0] > 0]

    ax6.axvline(HIGH_GAIN_SATURATION, color='red', linewidth=0.4, label='HG saturation')
    ax6.axvline(1, color='green', linewidth=0.5, label='1mA')

    ax6.plot(isel, vsel/(isel/1e3), marker='.',
             label="resistance low gain", color='black', alpha=0.2)

    mmsel = MMcurrent[current[1] > 0]
    vsel = voltage[1][current[1] > 0]
    isel = current[1][current[1] > 0]

    ax6.plot(isel, vsel/(isel/1e3), marker='.',
             label="resistance high gain", color='blue')

    ax6.set_xlim([0,10])
    ax6.set_ylim([110,130])

    ax6.set_ylabel("measured resistance / Ohm")
    ax6.set_xlabel("OFM current / mA")
    ax6.set_title("Resistance matching before offset correction")

    ax6.legend()

    fig.tight_layout()
    plt.show()

    ###########################################################################

    fig, ax7 = plt.subplots(2, 2, figsize=(6,10))

    ax7 = ax7.reshape( (4,) )

    ax7[0].plot(current[1], current[0], marker='')
    ax7[0].set_xlabel("HG current / mA")
    ax7[0].set_ylabel("LG current / mA")
    ax7[0].plot([0,5], [0,5])
    ax7[0].set_ylim([0,3.5])
    ax7[0].set_xlim([0,3.5])

    ax7[1].plot(current[1], current[1]-current[0], marker='')
    ax7[1].set_xlabel("HG current / mA")
    ax7[1].set_ylabel("HG - LG current / mA")
    ax7[1].axhline(0)
    ax7[1].set_ylim([-0.15, 0.15])
    ax7[1].set_xlim([0,3.5])

    ax7[2].plot(voltage[1], voltage[0], marker='')
    ax7[2].set_xlabel("HG voltage / V")
    ax7[2].set_ylabel("LG voltage / V")
    ax7[2].plot([0,5], [0,5])
    ax7[2].set_ylim([0,0.35])
    ax7[2].set_xlim([0,0.35])

    ax7[3].plot(voltage[1], voltage[1]-voltage[0], marker='')
    ax7[3].set_xlabel("HG voltage / V")
    ax7[3].set_ylabel("HG - LG voltage / V")
    ax7[3].axhline(0)
    ax7[3].set_ylim([-0.02,0.02])
    ax7[3].set_xlim([0,0.35])

    U_HG_LG = voltage[1]-voltage[0]

    selection  = voltage[1] > 0.02
    selection2 = voltage[1] < 0.33
    selection = selection & selection2

    U_HG_LG = U_HG_LG[ selection ]
    U_HG_LG = np.median(U_HG_LG)
    ax7[3].axhline(U_HG_LG, color='red')
    print("Offset U", U_HG_LG)

    ax7[2].plot(voltage[1], voltage[0]+U_HG_LG, marker='')
    ax7[3].plot(voltage[1][selection],
                voltage[1][selection] - (voltage[0][selection] + U_HG_LG), marker='')

    ###########################################################################
    # current offset

    I_HG_LG = current[1]-current[0]

    selection  = current[1] > 0.2
    selection2 = current[1] < HIGH_GAIN_SATURATION
    selection = selection & selection2

    I_HG_LG = I_HG_LG[ selection ]
    I_HG_LG = np.median(I_HG_LG)
    ax7[1].axhline(I_HG_LG, color='red')
    print("Offset I", I_HG_LG)

    ax7[0].plot(current[1], current[0]+I_HG_LG, marker='')
    ax7[1].plot(current[1][selection],
                current[1][selection] - (current[0][selection] + I_HG_LG), marker='')
    ax7[1].axvline(HIGH_GAIN_SATURATION)

    fig.tight_layout()
    plt.show()

    with open("bias_settings.txt", "a") as myfile:
        myfile.write("%s\t%f\t%f\n"%(filename, U_HG_LG, I_HG_LG))

    ###########################################################################
    # plot corrected resistance

    fig, ax8 = plt.subplots()

    mmsel = MMcurrent[current[0] > 0]
    vsel = voltage[0][current[0] > 0] + U_HG_LG
    isel = current[0][current[0] > 0] + I_HG_LG

    ax8.axvline(HIGH_GAIN_SATURATION, color='red', linewidth=0.4, label='HG saturation')
    ax8.axvline(1, color='green', linewidth=0.5, label='1mA')

    ax8.plot(isel, vsel/(isel/1e3), marker='.',
             label="resistance low gain\n"+
                     "Ubias = %6.4f\n"%(U_HG_LG) +
                     "Ibias = %6.4f"%(I_HG_LG)
             , color='black', alpha=0.2)

    R_LG = vsel/(isel/1e3)

    mmsel = MMcurrent[current[1] > 0]
    vsel = voltage[1][current[1] > 0]
    isel = current[1][current[1] > 0]

    ax8.plot(isel, vsel/(isel/1e3), marker='.',
             label="resistance high gain", color='blue')

    ax8.set_xlim([0,20])

    R = np.mean(R_LG)
    ax8.axhline(R, color="green", label="Mean resistance (%5.2f Ohm)"%(R))
    ax8.set_ylim([ R - 1.5 , R + 1.5])

    ax8.set_ylabel("measured resistance / Ohm")
    ax8.set_xlabel("OFM current / mA")
    ax8.set_title("Resistance matching after offsets")

    ax8.legend()

    fig.tight_layout()
    plt.savefig(filename.replace('.npz', '_Rmatching_final.png'))
    plt.show()

    ###########################################################################

    fig, ax9 = plt.subplots(2, 2, figsize=(6,10))

    ax9 = ax9.reshape( (4,) )

    U_SATURATION_LSB = 3970
    U_SATURATION = convertVoltage(U_SATURATION_LSB, 1)

    I_SATURATION_LSB = 3970
    I_SATURATION = convertCurrent(I_SATURATION_LSB, 1) * 1e3

    ax9[0].plot(dac_steps, current[0] + I_HG_LG, marker='', label="LG current + offset")
    ax9[0].plot(dac_steps, current[1], marker='', label="HG current")
    ax9[0].axhline( I_SATURATION )
    ax9[0].set_xlabel("DAC setpoint / LSB")
    ax9[0].set_ylabel("current / mA")
    #ax9[0].plot([0,5], [0,5])
    ax9[0].set_ylim([0,4])
    ax9[0].set_xlim([0,5*33])

    ax9[1].plot(dac_steps[current[1] < I_SATURATION], current[1][current[1] < I_SATURATION]-(current[0][current[1] < I_SATURATION]+I_HG_LG), marker='')
    ax9[1].set_xlabel("DAC setpoint / LSB")
    ax9[1].set_ylabel("HG - LG current / mA")
    ax9[1].axhline(0)
    ax9[1].set_ylim([-0.05, 0.05])
    ax9[1].set_xlim([0,5*33])

    ax9[2].plot(dac_steps, voltage[0] + U_HG_LG, marker='', label="LG voltage + offset")
    ax9[2].plot(dac_steps, voltage[1], marker='', label="HG voltage")
    ax9[2].axhline( U_SATURATION )

    ax9[2].set_xlabel("DAC setpoint / LSB")
    ax9[2].set_ylabel("LG voltage / V")
    #ax9[2].plot([0,5], [0,5])
    ax9[2].set_ylim([0,0.5])
    ax9[2].set_xlim([0,5*33])

    ax9[3].plot(dac_steps[voltage[1] < U_SATURATION], voltage[1][voltage[1] < U_SATURATION]-(voltage[0][voltage[1] < U_SATURATION] + U_HG_LG), marker='')
    ax9[3].set_xlabel("DAC setpoint / LSB")
    ax9[3].set_ylabel("HG - LG voltage / V")
    ax9[3].axhline(0)
    ax9[3].set_ylim([-0.005,0.005])
    ax9[3].set_xlim([0,5*33])

    for i in range(4):
        ax9[i].legend()

    fig.tight_layout()
    #plt.savefig(filename.replace('.npz', '_Rmatching_final.png'))
    plt.show()


if __name__ == "__main__":

    #plot_calibration("calibration_20230104_085105_CH0_10.npz")
    #plot_calibration("calibration_20230104_094358_CH0_10.npz")
    #plot_calibration('calibration_20230104_100702_CH0_10.npz')
    plot_calibration("calibration_20230105_083834_CH0_2.npz")
    print('#'*40)
    print('CHANNEL0')
    plot_calibration('calibration_20230104_105710_CH0_20.npz')
    print('#'*40)
    print('CHANNEL1')
    #plot_calibration('calibration_20230104_113819_CH1_20.npz')
    plot_calibration('calibration_20230104_122100_CH1_20.npz')
