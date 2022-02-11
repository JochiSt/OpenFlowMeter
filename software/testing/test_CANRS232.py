# -*- coding: utf-8 -*-

import sys
sys.path.append("../pyUSBtin")
from pyusbtin.usbtin import USBtin
from pyusbtin.canmessage import CANMessage

sys.path.append("../")
from OpenFlowMeter import OpenFlowMeter

from time import sleep

def log_data(msg):
    #print("Message ID %x"%(msg.mid) )
    #print("length %d"%(msg.dlc) )
    if msg.mid == 0x123:
        if msg.dlc == 8:
            print(msg)


usbtin = USBtin()
usbtin.connect("COM7")
usbtin.add_message_listener(log_data)
usbtin.open_can_channel(500000, USBtin.ACTIVE)

DACsettings = [0]*4

#usbtin.send(CANMessage(0x123, DACsettings))

def main():

    ofm =  OpenFlowMeter(usbtin = usbtin, boardID=0x1)

    try:
        while True:
            try:
                # input channel and value
                channel = int( input("channel (0,1): ") )
                # if channel < 0 exit loop
                if channel < 0:
                    break

                # if channel > 1 do nothing
                if channel > 1:
                    print("channel larger 1")
                    continue

                value = int (input("value 0 - 1023: ") )
            except Exception:
                continue

            if value > 1023 or value < 0:
                print("value not between 0 and 1023")
                continue

            # set channel and send out via CAN
            # inside STM32
            #       uint16_t pwm1 = RxData[0] <<8 | RxData[1];
            #       uint16_t pwm2 = RxData[2] <<8 | RxData[3];
            DACsettings[2 * channel      ] = ( value >> 8)
            DACsettings[2 * channel +1 ] = ( value & 0xFF )

            canmessage = CANMessage(mid=0x123, dlc=4, data=DACsettings.copy() )
            print(canmessage)
            usbtin.send(canmessage)

    except KeyboardInterrupt:
        pass

    # shutting down CAN interface
    usbtin.stop_rx_thread()
    usbtin.close_can_channel()
    # disconnect from USBtin
    usbtin.disconnect()

if __name__ == "__main__":
    main()

