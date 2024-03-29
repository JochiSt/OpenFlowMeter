# -*- coding: utf-8 -*-
"""

"""

import sys,os

from .OpenFlowMeter_Config import OpenFlowMeter_Config

sys.path.append( os.path.dirname(os.path.realpath(__file__)) + "../pyUSBtin")
sys.path.append("../pyUSBtin")
from pyusbtin.canmessage import CANMessage
import time
import copy

import numpy as np

class OpenFlowMeter(object):
    """
        Class for handling the OpenFlowMeter using USBTIN with python
    """

    CHANGE_CFG_DELAY    = 0.05

    # message IDs (have to match those in can.h)
    CAN_CONFIG_ID       = 0x100     # handling of the configuration register
    CAN_UC_STATUS       = 0x101     # microcontroller status
    CAN_DAC_ID          = 0x102     # DAC setpoints
    CAN_ADC_MSG_ID_CH0  = 0x103     # ADC channel 0
    CAN_ADC_MSG_ID_CH1  = 0x104     # ADC channel 1
    CAN_TEMPERATURE_ID  = 0x105     # calculated temperatures (2x float)
    CAN_VOLTAGE_ID      = 0x106     # calculated voltage (2x float)
    CAN_CURRENT_ID      = 0x107     # calculated current (2x float)
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
        self.DACsetting  = [0]*2
        self.DACreadback = [None]*2

        self._current_0 = [0]*2
        self._voltage_0 = [0]*2

        self._current_1 = [0]*2
        self._voltage_1 = [0]*2

        self.uCtemperature = 0
        self.uCrefvoltage  = 0

        self.temperatures = [0]*2
        self.voltages = [0]*2
        self.currents = [0]*2
        self.ADCgains = 0

        self.TMP100_T = 0

        self.hasNewMessage = False

        self.config = OpenFlowMeter_Config()
        self.config.boardID = boardID
        # store configuration, which is in the device
        self._deviceconfig = copy.deepcopy(self.config)

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

        elif msg.mid == OpenFlowMeter.CAN_DAC_ID | (self.config.boardID << 4):  # DAC readback
            if msg.dlc < 6:
                return
            self.DACreadback[0] = (msg[0] << 8)  + msg[1]
            self.DACreadback[1]  = (msg[2] << 8)  + msg[3]
            self.ADCgains = (msg[4] << 8)  + msg[5]

        elif msg.mid == OpenFlowMeter.CAN_I2C_MSG_TMP100 |  (self.config.boardID << 4):
            if msg.dlc > 2:
                return
            self.TMP100_T =  ((msg[0] << 8)  + msg[1] ) * 0.0625;

        elif msg.mid == OpenFlowMeter.CAN_TEMPERATURE_ID | (self.config.boardID << 4):
            if msg.dlc != 8:
                return
            self.temperatures = np.frombuffer( bytearray([ data for data in msg ]), dtype=np.float32)

        elif msg.mid == OpenFlowMeter.CAN_VOLTAGE_ID | (self.config.boardID << 4):
            if msg.dlc != 8:
                return
            self.voltages = np.frombuffer( bytearray([ data for data in msg ]), dtype=np.float32)

        elif msg.mid == OpenFlowMeter.CAN_CURRENT_ID | (self.config.boardID << 4):
            if msg.dlc != 8:
                return
            self.currents = np.frombuffer( bytearray([ data for data in msg ]), dtype=np.float32)

        elif msg.mid == OpenFlowMeter.CAN_CONFIG_ID | (self.config.boardID << 4):
            if msg.dlc == 2:
                #print(msg[0], msg[1], end="", flush=True)
                try:
                    self.config[msg[0]] = msg[1]
                    self._deviceconfig[msg[0]] = msg[1]
                except IndexError:
                    #print(" <- ", end="", flush=True)
                    pass
                #print()
            else:
                print(msg)
        else:
            #print("%ld Message ID 0x%x not implemented"%(time.time(), msg.mid))
            return

        self.hasNewMessage = True

        #print("OFM", msg)
        #for i in [0, 1]:
        #   print(self._current_0[i], self._voltage_0[i])

    def setDAC(self, channel0, channel1):
        """
        Set the values for both DACs

        Parameters
        ----------
        channel1 : int
            DESCRIPTION.
        channel2 : int
            DESCRIPTION.

        Returns
        -------
        None.

        """
        # inside STM32
        #       uint16_t pwm1 = RxData[0] <<8 | RxData[1];
        #       uint16_t pwm2 = RxData[2] <<8 | RxData[3];
        if channel0 is not None:
            self.DACsetting[0] = channel0
        else:
            if self.DACreadback[0] is not None:
                self.DACsetting[0] = self.DACreadback[0]
            else:
                self.DACsetting[0] = 0
        if channel1 is not None:
            self.DACsetting[1] = channel1
        else:
            if self.DACreadback[1] is not None:
                self.DACsetting[1] = self.DACreadback[1]
            else:
                self.DACsetting[1] = 0

        DACsettings = [0]*4
        for chan in [0,1]:
            DACsettings[2 * chan    ] = ( self.DACsetting[chan] >> 8)
            DACsettings[2 * chan +1 ] = ( self.DACsetting[chan] & 0xFF )

        canmessage = CANMessage(mid=OpenFlowMeter.CAN_DAC_ID | (self.config.boardID << 4),
                                dlc=4, data=DACsettings.copy() )
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
        """
        request transmission of the full configuration

        Returns
        -------
        None.

        """
        # trigger sending the current configuration
        canmessage = CANMessage( mid=OpenFlowMeter.CAN_CONFIG_ID | (self.config.boardID << 4),
                                dlc=8,
                                data=[0x12,0x34,0x56,0x78,0x90,0x01,0xFF,0xFD])
        self.usbtin.send(canmessage)

    def changeConfig(self, everything=False):
        """
        send the full configuration to the OpenFlowMeter. This is not stored
        inside the EEPROM unless the OFM is told to do so.

        Returns
        -------
        None.

        """
        if everything:
            for i, byte in enumerate(self.config.toBytes()):
                canmessage = CANMessage( mid=OpenFlowMeter.CAN_CONFIG_ID | (self.config.boardID << 4),
                                        dlc=8,
                                        data=[0x12,0x34,0x56,0x78,0x90,0x01, i, byte])
                self.usbtin.send(canmessage)
                time.sleep(OpenFlowMeter.CHANGE_CFG_DELAY)
        else:
            for i, byte in self._deviceconfig.delta(self.config):
                canmessage = CANMessage( mid=OpenFlowMeter.CAN_CONFIG_ID | (self.config.boardID << 4),
                                        dlc=8,
                                        data=[0x12,0x34,0x56,0x78,0x90,0x01, i, byte])
                self.usbtin.send(canmessage)
                time.sleep(OpenFlowMeter.CHANGE_CFG_DELAY)
