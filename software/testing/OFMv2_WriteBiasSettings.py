# -*- coding: utf-8 -*-

import sys
sys.path.append("../")
from OpenFlowMeter import OpenFlowMeter

from CANsetup import CANsetup

import time


def GetConfigFromDevice():
    setup = None
    try:
        print("Getting the configuration from OFM")
        # initialise USBtin
        setup = CANsetup()

        # initialise OFM
        ofm =  OpenFlowMeter(usbtin = setup.usbtin, boardID=0x1)
        #ofm.saveCofig2EEPROM(default=1)     # save the default config in EEPROM

        ofm.requestConfigFromDevice()
        time.sleep(5)
        ofm.config.printout()

        with open("bias_settings.txt") as myfile:
            lines = myfile.readlines()
            for line in lines:
                split = line.split('\t')
                Ubias = float(split[1])
                Ibias = float(split[2]) # in mA
                if 'CH0' in line:
                    channel = 0
                elif 'CH1' in line:
                    channel = 1
                else:
                    print("Channel not found")
                    continue

                ofm.config.Ibias[channel] = Ibias
                ofm.config.Ubias[channel] = Ubias

        print("Change Configuration")
        ofm.changeConfig()

        print("Save Config into EEPROM")
        ofm.saveCofig2EEPROM()

        print("config saved")

    except Exception as e:
        print(e)
        pass

    finally:
        if setup:
            setup.deinit()

if __name__ == "__main__":
    GetConfigFromDevice()


