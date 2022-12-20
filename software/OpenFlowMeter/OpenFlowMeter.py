# -*- coding: utf-8 -*-
"""

"""

import sys,os

from .OpenFlowMeter_Config import OpenFlowMeter_Config

sys.path.append( os.path.dirname(os.path.realpath(__file__)) + "../pyUSBtin")
sys.path.append("../pyUSBtin")
from pyusbtin.canmessage import CANMessage
import time

class OpenFlowMeter(object):
    """
        Class for handling the OpenFlowMeter using USBTIN with python
    """

    # message IDs (have to match those in can.h)
    CAN_CONFIG_ID       = 0x100     # handling of the configuration register
    CAN_UC_STATUS       = 0x101     # microcontroller status
    CAN_DAC_ID          = 0x102     # DAC setpoints
    CAN_ADC_MSG_ID_CH0  = 0x103     # ADC channel 0
    CAN_ADC_MSG_ID_CH1  = 0x104     # ADC channel 1
    CAN_I2C_MSG_TMP100  = 0x108     # on board TMP100
    CAN_I2C_MSG_BME680  = 0x109     # on board BME680

    def __init__(self, usbtin, boardID):
        """


        Parameters
        ----------
        usbtin : usbtin
            USB CAN interface
        boardID : int
            Board ID of the connected OpenFlowMeter.

        Returns
        -------
        None.

        """
        self.usbtin = usbtin
        self.DACsettings = [0]*4

        self._current_0 = [0]*2
        self._voltage_0 = [0]*2

        self._current_1 = [0]*2
        self._voltage_1 = [0]*2

        self.uCtemperature = 0
        self.uCrefvoltage  = 0

        self.hasNewMessage = False

        self.config = OpenFlowMeter_Config()
        self.config.boardID = boardID

        # register this module to the USBtin interface
        self.usbtin.add_message_listener(self.handleCANmessage)

    def voltage(self, channel, gain=0):
        """
            returns the measured voltage across the PT100 resistor

        Parameters
        ----------
        channel : int
            selects channel 0 or channel 1.
        gain : int, optional
            gain setting of the switchable gain amplifier.
            The default is 0.

        Returns
        -------
        int
            raw voltage output.

        """
        if gain == 0:
            return self._voltage_0[channel]
        else:
            return self._voltage_1[channel]

    def current(self, channel, gain=0):
        """
            returns the measured current via the PT100 resistor

        Parameters
        ----------
        channel : int
            selects channel 0 or channel 1.
        gain : int, optional
            gain setting of the switchable gain amplifier.
            The default is 0.

        Returns
        -------
        int
            raw current output.

        """
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

        if msg.mid == OpenFlowMeter.CAN_ADC_MSG_ID_CH0 | (self.config.boardID << 4):    # channel 0
            if msg.dlc < 8:
                return
            self._current_0[0] = (msg[0] << 8)  + msg[1]
            self._voltage_0[0] = (msg[2] << 8)  + msg[3]
            self._current_1[0] = (msg[4] << 8)  + msg[5]
            self._voltage_1[0] = (msg[6] << 8)  + msg[7]

        elif msg.mid == OpenFlowMeter.CAN_ADC_MSG_ID_CH1 | (self.config.boardID << 4):  # channel 1
            if msg.dlc < 8:
                return
            self._current_0[1] = (msg[0] << 8)  + msg[1]
            self._voltage_0[1] = (msg[2] << 8)  + msg[3]
            self._current_1[1] = (msg[4] << 8)  + msg[5]
            self._voltage_1[1] = (msg[6] << 8)  + msg[7]

        elif msg.mid == OpenFlowMeter.CAN_UC_STATUS | (self.config.boardID << 4):  # uC status
            if msg.dlc < 4:
                return
            self.uCtemperature = (msg[0] << 8)  + msg[1]
            self.uCrefvoltage  = (msg[2] << 8)  + msg[3]

        elif msg.mid == OpenFlowMeter.CAN_CONFIG_ID | (self.config.boardID << 4):
            if msg.dlc == 2:
                cfgbytes = self.config.toBytes()

                print(msg[0], msg[1], end="", flush=True)
                if (msg[0] < len(cfgbytes)):
                    cfgbytes[msg[0]] = msg[1]
                else:
                    print(" <- ", end="", flush=True)
                print()
                self.config.fromBytes(cfgbytes)
            else:
                print(msg)
        else:
            #print("%ld Message ID 0x%x not implemented"%(time.time(), msg.mid))
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

            canmessage = CANMessage(mid=OpenFlowMeter.CAN_DAC_ID | (self.config.boardID << 4),
                                    dlc=4, data=self.DACsettings.copy() )
            # print(canmessage)
            self.usbtin.send(canmessage)

    def saveCofig2EEPROM(self, default=0):
        """
        Tell the OFM to save the current configuration inside the EEPROM


        Parameters
        ----------
        default : int, optional
            If this is 1 the default config is written into the EEPROM.
            The default is 0.

        Returns
        -------
        None.

        """

        canmessage = CANMessage( mid=OpenFlowMeter.CAN_CONFIG_ID | (self.config.boardID << 4),
                                dlc=8,
                                data=[0x12,0x34,0x56,0x78,0x90,0x01,0xFF, 0xFE + default])
        self.usbtin.send(canmessage)


    def requestConfigFromDevice(self):
        # trigger sending the current configuration
        canmessage = CANMessage( mid=OpenFlowMeter.CAN_CONFIG_ID | (self.config.boardID << 4),
                                dlc=8,
                                data=[0x12,0x34,0x56,0x78,0x90,0x01,0xFF,0xFD])
        self.usbtin.send(canmessage)

    def changeConfig(self):
        for i, byte in enumerate(self.config.toBytes()):
            canmessage = CANMessage( mid=OpenFlowMeter.CAN_CONFIG_ID | (self.config.boardID << 4),
                                    dlc=8,
                                    data=[0x12,0x34,0x56,0x78,0x90,0x01, i, byte])
            self.usbtin.send(canmessage)
