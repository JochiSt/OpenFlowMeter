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
        time.sleep(1)

        ofm.config.interval_I2C_TMP100 = 1

        ofm.config.PID_flags = 0b00000000

        # PID settings channel 0
        ofm.config.PID_T[0] = 40.0
        ofm.config.PID_P[0] = 0.9
        ofm.config.PID_I[0] = 0
        ofm.config.PID_D[0] = 0

        # PID settings channel 1
        ofm.config.PID_T[1] = 40.0
        ofm.config.PID_P[1] = 0
        ofm.config.PID_I[1] = 0
        ofm.config.PID_D[1] = 0

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
        dac_0 = np.array([])
        dac_1 = np.array([])

        r_0 = [np.array([]), np.array([])]
        r_1 = [np.array([]), np.array([])]

        print("Use CTRL-C to stop datataking...")

        dac_on = False

        try:
            while True:
                ofm.waitForNewMessage()
                ofm.hasNewMessage = False

                runtime = time.time()-time0

                if runtime > 20 and runtime < 120 and not dac_on:
                    dac_on = True
                    ofm.setDAC(1023, 1023)

                if runtime > 120 and dac_on:
                    dac_on = False
                    ofm.setDAC(10,10)

                if runtime > 240:   # exit after 4 minutes
                    break

                timestamp = np.append(timestamp, runtime)
                t_tmp100 = np.append(t_tmp100, ofm.TMP100_T)

                dac_0 = np.append(dac_0, ofm.DACreadback[0])
                dac_1 = np.append(dac_1, ofm.DACreadback[1])

                for gain in [0,1]:
                    # prevent division by zero
                    i_0 = ofm.current(0,gain)
                    i_1 = ofm.current(1,gain)

                    u_0 = ofm.voltage(0,gain)
                    u_1 = ofm.voltage(1,gain)

                    if i_0 < 4020 and u_0 < 4020:  # exclude the saturation points
                        u_0 = convertVoltage(u_0)
                        i_0 = convertCurrent(max(i_0, 0.00001))
                        r_0[gain] = np.append(r_0[gain], u_0 / i_0)
                    else:
                        r_0[gain] = np.append(r_0[gain], np.nan)

                    if i_1 < 4020 and u_1 < 4020:  # exclude the saturation points
                        u_1 = convertVoltage(u_1)
                        i_1 = convertCurrent(max(i_1, 0.00001))
                        r_1[gain] = np.append(r_1[gain], u_1 / i_1)

                    else:
                        r_1[gain] = np.append(r_1[gain], np.nan)

        except KeyboardInterrupt:
            pass

        except Exception as e:
            print(e)

        ofm.setDAC(10,10)

        fig, ax = plt.subplots(2, 1, figsize=(6,10))

        color = 'tab:blue'
        for i in [0,1]:
            ax[i].plot( timestamp, t_tmp100, label="T TMP100", color='lightsteelblue')
            ax[i].set_ylabel("Temperature / degC", color=color)
            ax[i].tick_params(axis='y', labelcolor=color)

        for gain in [0,1]:
            colors = ['mediumblue', 'cornflowerblue']
            ax[0].plot( timestamp, PT100.convertPT100_T(r_0[gain]),
                       label="T CH0 gain %d"%(gain), color=colors[gain])
            ax[1].plot( timestamp, PT100.convertPT100_T(r_1[gain]),
                       label="T CH1 gain %d"%(gain), color=colors[gain])

        ax2 = [
            ax[0].twinx(),
            ax[1].twinx()
            ]

        color = 'tab:orange'
        for i in [0,1]:
            ax2[i].set_ylabel("DAC setpoint / LSB", color=color)
            ax2[i].tick_params(axis='y', labelcolor=color)

        ax2[0].plot( timestamp, dac_0, label="DAC CH0", color=color)
        ax2[1].plot( timestamp, dac_1, label="DAC CH1", color=color)

        ax3 = [
            ax[0].twinx(),
            ax[1].twinx()
            ]

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


