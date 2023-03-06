# -*- coding: utf-8 -*-
"""

"""
import sys
sys.path.append("../../software")
sys.path.append("../../software/pyUSBtin")  # needed for OpenFlowMeter
from OpenFlowMeter import PT100
from OpenFlowMeter import convertVoltage, convertCurrent, U2LSB, I2LSB


def I2U(I):
    return I / 10e-3   # voltage output of currentsensing

def OffsetAmp(Uin, Uoffset, R1, R2):
    return Uoffset + (Uin - Uoffset)*(1+R1/R2)

GAIN_I = 1 + 47e3/5.6e3
GAIN_U = 1 + 33e3/5.6e3

LSB2U = 3.3 / 4096;
LSB2I = 3.3 / 4096 * 10e-3;

temperature = 40

R_PT100 = PT100.convertPT100_R(temperature)
print("Temperature", temperature, "degC", "PT100", R_PT100, "Ohm")



Ibias = 20e-3 - 0.3e-3
IbiasU = I2U(Ibias)

Uoffset = IbiasU * 1.1

Upt100 = R_PT100 * Ibias

print("Voltages before amplification:")
print("U", Upt100, "I", IbiasU)
print()

Upt100 = OffsetAmp(Upt100, Uoffset, 47e3, 5.6e3)
IbiasU = OffsetAmp(IbiasU, Uoffset, 33e3, 5.6e3)

print("Voltages after amplification:")
print("U", Upt100, "I", IbiasU)
print()

Upt100LSB = U2LSB(Upt100)
Ipt100LSB = U2LSB(IbiasU)

print("LSB inside the ADC")
print("U", Upt100LSB, "I", Ipt100LSB)