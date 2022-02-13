# -*- coding: utf-8 -*-
"""

"""

import sys,os
sys.path.append( os.path.dirname(os.path.realpath(__file__)) + "/pyUSBtin")
from pyusbtin.usbtin import USBtin
from pyusbtin.canmessage import CANMessage

class OpenFlowMeter(object):
    """
        Class for handling the OpenFlowMeter using USBTIN with python
    """

    def __init__(self, usbtin, boardID):
        """
            init function
        """
        self.usbtin = usbtin
        self.boardID = boardID
        self.DACsettings = [0]*4

        self._current = [0]*2
        self._voltage = [0]*2

        self.hasNewMessage = False

        # register this module to the USBtin interface
        self.usbtin.add_message_listener(self.handleCANmessage)

    def voltage(self, channel):
        return self._voltage[channel]

    def current(self, channel):
        return self._current[channel]

    def handleCANmessage(self, msg):
        """"
            handle a can message from USBtin
        """
        # first check, that the message belongs to our module

        # for(uint8_t i = 0; i<4; i++){
        #  data[2*i    ] = upper(adcBuf[i]);
        #  data[2*i + 1] = lower(adcBuf[i]);
        # }
        if msg.dlc < 8:
            return

        self._current[0] = (msg[0] << 8)  + msg[1]
        self._voltage[0] = (msg[2] << 8)  + msg[3]
        self._current[1] = (msg[4] << 8)  + msg[5]
        self._voltage[1] = (msg[6] << 8)  + msg[7]

        self.hasNewMessage = True

        #print("OFM", msg)
        #for i in [0, 1]:
        #   print(self._current[i], self._voltage[i])

    def setDAC(self, channel1, channel2):
            """
                set values for both DACs
            """
            # set channel and send out via CAN
            # inside STM32
            #       uint16_t pwm1 = RxData[0] <<8 | RxData[1];
            #       uint16_t pwm2 = RxData[2] <<8 | RxData[3];
            DACset = [channel1, channel2]
            for chan in [0,1]:
                self.DACsettings[2 * chan      ] = ( DACset[chan] >> 8)
                self.DACsettings[2 * chan +1 ] = ( DACset[chan] & 0xFF )

            canmessage = CANMessage(mid=0x123, dlc=4, data=self.DACsettings.copy() )
            # print(canmessage)
            self.usbtin.send(canmessage)