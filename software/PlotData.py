# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt

def plotVoltageVsDAC(dac, voltage):
    plt.plot(dac, voltage, label="U")
    plt.xlabel('DAC / LSB')
    plt.ylabel('voltage / V')
    plt.legend()
    plt.show()

def plotCurrentVsDAC(dac, current):
    plt.plot(dac, current*1000, label="I")
    plt.xlabel('DAC / LSB')
    plt.ylabel('current / mA')
    plt.legend()
    plt.show()

def plotResistanceVsDAC(dac, voltage, current):
    resistance = voltage / current
    plt.plot(dac[1:], resistance[1:], label="R")
    plt.ylabel('R / Ohm')
    plt.xlabel('DAC / LSB')
    plt.legend()

    #plt.ylim([90,100])

    plt.show()