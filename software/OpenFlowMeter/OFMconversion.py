# -*- coding: utf-8 -*-

def convertCurrent(lsb):
    return lsb * 3.3/4095 * 10e-3

def convertVoltage(lsb):
    return lsb * 3.3/4095