# -*- coding: utf-8 -*-

import sys
sys.path.append("../")
from OpenFlowMeter import OpenFlowMeter
from OpenFlowMeter import PT100
from OpenFlowMeter import convertVoltage, convertCurrent
from CANsetup import CANsetup

import matplotlib.pyplot as plt
import numpy as np

import time

def main():
    setup = None
    try:
        print("Getting the configuration from OFM")
        print('#'*70+'\n')

        # initialise USBtin
        setup = CANsetup()

        # initialise OFM
        ofm =  OpenFlowMeter(usbtin = setup.usbtin, boardID=0x1)
        ofm.requestConfigFromDevice()
        time.sleep(2)
        ofm.requestConfigFromDevice()
        time.sleep(2)
        ofm.requestConfigFromDevice()
        time.sleep(2)

        ofm.config.interval_I2C_TMP100 = 64

        ofm.config.PID_flags = 0b00000000

        # PID settings channel 0
        ofm.config.PID_T[0] = 40.0
        ofm.config.PID_P[0] = 0
        ofm.config.PID_I[0] = 0
        ofm.config.PID_D[0] = 0

        # PID settings channel 1
        ofm.config.PID_T[1] = 30.0
        ofm.config.PID_P[1] = 4
        ofm.config.PID_I[1] = 0.00002
        ofm.config.PID_D[1] = 0.1

        time.sleep(1)
        ofm.changeConfig()
        time.sleep(1)

        print('\n'+'#'*70+'\n')

        ofm.requestConfigFromDevice()
        time.sleep(1)
        ofm.config.printout()

        ofm.setDAC(10, 10)
        time.sleep(2)

        time0 = time.time()
        timestamp = np.array([])

        t_tmp100 = np.array([])
        dac  = [np.array([]), np.array([])]
        setp = [np.array([]), np.array([])]
        temperatures = [np.array([]), np.array([])]
        r_0  = [np.array([]), np.array([])]
        r_1  = [np.array([]), np.array([])]

        sat_i_0 = 0
        sat_u_0 = 0
        sat_i_1 = 0
        sat_u_1 = 0

        i_0 = [0]*2
        u_0 = [0]*2
        i_1 = [0]*2
        u_1 = [0]*2

        print("Use CTRL-C to stop datataking...")

        dac_on = False

        TIME_START = 30
        TIME_PID_ACTIVE = 300
        TIME_STOP = 60

        # for debugging
        #TIME_START = 2
        #TIME_PID_ACTIVE = 10
        #TIME_STOP = 2

        TIME_DISTURB = 200
        disturbed = False

        try:
            while True:
                ofm.waitForNewMessage()
                ofm.hasNewMessage = False

                runtime = time.time()-time0

                if runtime > TIME_START and runtime < TIME_START + TIME_PID_ACTIVE  and not dac_on:
                    dac_on = True
                    ofm.config.PID_active[1] = True
                    ofm.changeConfig()
                    print("PID enabled")

                if runtime > TIME_START + TIME_PID_ACTIVE and dac_on:
                    dac_on = False
                    ofm.config.PID_active[1] = False
                    ofm.changeConfig()
                    print("PID disabled")

                    ofm.setDAC(10,10)

                if runtime > TIME_START + TIME_PID_ACTIVE + TIME_STOP:
                    break

                if runtime > TIME_START + TIME_DISTURB and not disturbed:
                    print("Changing setpoint of PID")
                    disturbed = True
                    ofm.config.PID_T[1] = ofm.config.PID_T[1] + 10
                    ofm.changeConfig()

                timestamp = np.append(timestamp, runtime)
                t_tmp100 = np.append(t_tmp100, ofm.TMP100_T)

                for ch in [0,1]:
                    dac[ch]  = np.append(dac[ch], ofm.DACreadback[ch])
                    setp[ch] = np.append(setp[ch], ofm.config.PID_T[ch])
                    temperatures[ch] = np.append(temperatures[ch], ofm.temperatures[ch])

                for gain in [0,1]:

                    i_0[gain] = ofm.current(0,gain)
                    i_1[gain] = ofm.current(1,gain)

                    u_0[gain] = ofm.voltage(0,gain)
                    u_1[gain] = ofm.voltage(1,gain)

                    # exclude the saturation points
                    sat_i_0 = i_0[gain] > 4020
                    sat_u_0 = u_0[gain] > 4020
                    sat_i_1 = i_1[gain] > 4020
                    sat_u_1 = u_1[gain] > 4020

                    u_0[gain] = convertVoltage(u_0[gain], gain)
                    # prevent division by zero
                    i_0[gain] = max( convertCurrent(i_0[gain], gain) , 0.00001)

                    u_1[gain] = convertVoltage(u_1[gain], gain)
                    # prevent division by zero
                    i_1[gain] = max( convertCurrent(i_1[gain], gain) , 0.00001)

                    # check for high gain setting, whether saturation has
                    # happened and if so, use the lower gain value
                    if gain == 1:
                        if sat_i_0:
                            i_0[gain] = i_0[0]
                        if sat_u_0:
                            u_0[gain] = u_0[0]

                        if sat_i_1:
                            i_1[gain] = i_1[0]
                        if sat_u_1:
                            u_1[gain] = u_1[0]

                    # only, if both are saturated ignore points
                    if sat_i_0 and sat_u_0:
                        r_0[gain] = np.append(r_0[gain], np.nan)
                    else:
                        r_0[gain] = np.append(r_0[gain], u_0[gain] / i_0[gain])

                    if sat_i_1 and sat_u_1:
                        r_1[gain] = np.append(r_1[gain], np.nan)
                    else:
                        r_1[gain] = np.append(r_1[gain], u_1[gain] / i_1[gain])

        except KeyboardInterrupt:
            pass

        except Exception as e:
            print(e)

        ofm.setDAC(10,10)
        ofm.config.PID_flags = 0b00000000
        ofm.changeConfig()

        fig, ax = plt.subplots(2, 1, figsize=(6,10))

        # temperatures
        color = 'tab:blue'
        for i in [0,1]:
            ax[i].plot( timestamp, t_tmp100, label="T TMP100", color='lightsteelblue')
            ax[i].set_ylabel("Temperature / degC", color=color)
            ax[i].tick_params(axis='y', labelcolor=color)

            ax[i].plot( timestamp, setp[i], label="setpoint")
            #ax[i].axhline(ofm.config.PID_T[i])

        for gain in [0,1]:
            colors = ['mediumblue', 'cornflowerblue']
            ax[0].plot( timestamp, PT100.convertPT100_T(r_0[gain]),
                       label="T CH0 gain %d"%(gain), color=colors[gain])
            ax[1].plot( timestamp, PT100.convertPT100_T(r_1[gain]),
                       label="T CH1 gain %d"%(gain), color=colors[gain])

        for i in [0,1]:
            ax[i].plot( timestamp, temperatures[i], label="calc. T", color='tab:deeppink')

        # DAC setpoint
        ax2 = [
            ax[0].twinx(),
            ax[1].twinx()
            ]

        color = 'tab:orange'
        for i in [0,1]:
            ax2[i].set_ylabel("DAC setpoint / LSB", color=color)
            ax2[i].tick_params(axis='y', labelcolor=color)
            ax2[i].plot( timestamp, dac[i], label="DAC", color=color)

        ax3 = [
            ax[0].twinx(),
            ax[1].twinx()
            ]

        # resistance
        color = 'tab:green'
        for i in [0,1]:
            ax3[i].set_ylabel("resistance / Ohm", color=color)
            ax3[i].spines['right'].set_position(('outward', 60))
            ax3[i].tick_params(axis='y', labelcolor=color)

        for gain in [0,1]:
            colors = ['forestgreen', 'lime']

            ax3[0].plot( timestamp, r_0[gain], label="R CH0 gain %d"%(gain),
                        color=colors[gain])
            ax3[1].plot( timestamp, r_1[gain], label="R CH1 gain %d"%(gain),
                        color=colors[gain])


        for i in [0,1]:
            ax[i].set_title("OFM PID test / evaluation Channel %d"%(i))
            ax[i].set_xlabel("measurement time / s")

        for i in [0,1]:
            ax[i].text(0.2, 0.95, "T %f\nP %f\nI %f\nD %f"%(
                    ofm.config.PID_T[i],
                    ofm.config.PID_P[i],
                    ofm.config.PID_I[i],
                    ofm.config.PID_D[i]
                ),
                 horizontalalignment='left',
                 verticalalignment='top',
                 transform=ax[i].transAxes,
                 fontfamily = 'monospace',
                 fontsize = 'medium')
            #ofm.config.PID_T[1] = 30.0

        #fig.legend()

        fig.tight_layout()
        plt.show()

    except Exception as e:
        print(e)
        pass

    finally:
        if setup:
            setup.deinit()

if __name__ == "__main__":
    main()


