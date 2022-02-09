# -*- coding: utf-8 -*-

import sys
sys.path.append("../pyUSBtin")

from pyusbtin.usbtin import USBtin
from pyusbtin.canmessage import CANMessage
from time import sleep

def log_data(msg):
    print("Message ID %x"%(msg.mid) )
    print("length %d"%(msg.dlc) )
    if msg.mid == 0x123:
        if msg.dlc == 8:
            print(msg)

usbtin = USBtin()
usbtin.connect("COM7")
usbtin.add_message_listener(log_data)
usbtin.open_can_channel(500000, USBtin.ACTIVE)

def main():
    try:
        while True:
            print("tick")

            #usbtin.send(CANMessage(0x123, [0, 0]))

            sleep(1)
    except KeyboardInterrupt:
        pass

    # shutting down CAN interface
    usbtin.stop_rx_thread()
    usbtin.close_can_channel()
    # disconnect from USBtin
    usbtin.disconnect()

if __name__ == "__main__":
    main()

