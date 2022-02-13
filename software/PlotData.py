# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

def plotVoltageVsDAC(dac, voltage):
    plt.plot(dac, voltage, label="U")
    plt.set_xlabel('DAC / LSB')
    plt.set_ylabel('voltage / V')
    plt.legend()
    plt.show()

def plotCurrentVsDAC(dac, current):
    plt.plot(dac, current, label="I")
    plt.set_xlabel('DAC / LSB')
    plt.set_ylabel('current / mA')
    plt.legend()
    plt.show()

def plotResistanceVsDAC(dac, voltage, current):
    resistance = voltage / current
    plt.plot(dac[1:], resistance[1:], label="R")
    plt.ylabel('R / LSB')
    plt.xlabel('DAC / LSB')
    plt.legend()
    plt.show()