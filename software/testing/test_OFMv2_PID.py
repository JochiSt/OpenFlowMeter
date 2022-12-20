# -*- coding: utf-8 -*-

import sys
sys.path.append("../")
from OpenFlowMeter import OpenFlowMeter
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
        #ofm.saveCofig2EEPROM(default=1)     # save the default config in EEPROM

        ofm.requestConfigFromDevice()
        time.sleep(1)
        ofm.config.printout()

        ofm.config.interval_I2C_TMP100 = 1

        ofm.config.PID_flags = 0b00000000

        # PID settings channel 0
        ofm.config.PID_P[0] = 0.9
        ofm.config.PID_I[0] = 0
        ofm.config.PID_D[0] = 0

        # PID settings channel 1
        ofm.config.PID_P[0] = 0
        ofm.config.PID_I[0] = 0
        ofm.config.PID_D[0] = 0

        ofm.changeConfig()

        print('\n'+'#'*70+'\n')

        time.sleep(1)
        ofm.config.printout()

        time0 = time.time()
        timestamp = np.array([])
        t_tmp100 = np.array([])

        print("Use CTRL-C to stop datataking...")
        try:
            while True:
                ofm.waitForNewMessage()
                ofm.hasNewMessage = False
                timestamp = np.append(timestamp, time.time()-time0)
                t_tmp100 = np.append(t_tmp100, ofm.TMP100_T)

        except KeyboardInterrupt:
            pass

        fig, (ax1) = plt.subplots(1, 1)

        ax1.plot( timestamp, t_tmp100, label="temperature TMP100", marker=".", linestyle = "-")

        ax1.set_title("Temperatures")
        ax1.set_xlabel("measurement time / s")
        ax1.set_ylabel("Temperature / degC")
        ax1.legend()

    except Exception as e:
        print(e)
        pass

    finally:
        if setup:
            setup.deinit()

if __name__ == "__main__":
    main()


