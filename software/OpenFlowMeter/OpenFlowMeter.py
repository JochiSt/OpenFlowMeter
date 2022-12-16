# -*- coding: utf-8 -*-
"""

"""

import sys,os
sys.path.append( os.path.dirname(os.path.realpath(__file__)) + "../pyUSBtin")
sys.path.append("../pyUSBtin")
from pyusbtin.canmessage import CANMessage
import time

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

        self._current_0 = [0]*2
        self._voltage_0 = [0]*2

        self._current_1 = [0]*2
        self._voltage_1 = [0]*2

        self.uCtemperature = 0
        self.uCrefvoltage  = 0

        self.hasNewMessage = False

        # register this module to the USBtin interface
        self.usbtin.add_message_listener(self.handleCANmessage)

    def voltage(self, channel, gain=0):
        if gain == 0:
            return self._voltage_0[channel]
        else:
            return self._voltage_1[channel]

    def current(self, channel, gain=0):
        if gain == 0:
            return self._current_0[channel]
        else:
            return self._current_1[channel]

    def uCtemperature(self):
        return self.uCtemperature

    def uCrefVoltage(self):
        return self.uCrefvoltage * 3300 / 4096

    def waitForNewMessage(self):
        """
            wait until a new mesage is received and parsed
        """
        while not self.hasNewMessage:
            time.sleep(0.1)

    def handleCANmessage(self, msg):
        """
            handle a can message from USBtin
        """
        # first check, that the message belongs to our module

        # for(uint8_t i = 0; i<4; i++){
        #  data[2*i    ] = upper(adcBuf[i]);
        #  data[2*i + 1] = lower(adcBuf[i]);
        # }

        """
            CAN message IDs from firmware
            #define CAN_ADC_MSG_ID_CH0  0x123
            #define CAN_ADC_MSG_ID_CH1  0x124
            #define CAN_STATUS_ID       0x120
        """
        if msg.mid == 0x123:    # channel 0
            if msg.dlc < 8:
                return
            self._current_0[0] = (msg[0] << 8)  + msg[1]
            self._voltage_0[0] = (msg[2] << 8)  + msg[3]
            self._current_1[0] = (msg[4] << 8)  + msg[5]
            self._voltage_1[0] = (msg[6] << 8)  + msg[7]

        elif msg.mid == 0x124:  # channel 1
            if msg.dlc < 8:
                return
            self._current_0[1] = (msg[0] << 8)  + msg[1]
            self._voltage_0[1] = (msg[2] << 8)  + msg[3]
            self._current_1[1] = (msg[4] << 8)  + msg[5]
            self._voltage_1[1] = (msg[6] << 8)  + msg[7]

        elif msg.mid == 0x120:  # uC status
            if msg.dlc < 4:
                return
            self.uCtemperature = (msg[0] << 8)  + msg[1]
            self.uCrefvoltage  = (msg[2] << 8)  + msg[3]

        else:
            print("Message ID 0x%x not implemented"%(msg.mid))
            return

        self.hasNewMessage = True

        #print("OFM", msg)
        #for i in [0, 1]:
        #   print(self._current_0[i], self._voltage_0[i])

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