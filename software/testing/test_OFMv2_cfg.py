# -*- coding: utf-8 -*-

import sys
sys.path.append("../")
from OpenFlowMeter import OpenFlowMeter

from CANsetup import CANsetup

import time


def main():
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

        ofm.config.interval_I2C_TMP100 = 64

        ofm.changeConfig()

        ofm.requestConfigFromDevice()
        time.sleep(5)
        ofm.config.printout()

    except Exception as e:
        print(e)
        pass

    finally:
        if setup:
            setup.deinit()

if __name__ == "__main__":
    main()


