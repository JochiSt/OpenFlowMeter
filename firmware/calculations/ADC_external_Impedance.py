# -*- coding: utf-8 -*-

import math

def Rext(TS, Fadc, Nbits=12):
    """
        returns the maximal allowed external impedance in kOhm
        see page 75 of https://www.st.com/resource/en/datasheet/stm32f103c8.pdf for details
    """

    print("TS = %.1f cycles\tFadc=%.2f MHz"%(TS, Fadc/1e6))
    Cadc = 8e-12
    Radc = 1e3
    RAIN = TS / (Fadc * Cadc * math.log (math.pow(2, Nbits+2)) ) - Radc
    return RAIN / 1000

print("Calculate the maximal allowed external impedance:")

TS = 55.5
Fadc = 6.75e6


print("%8.2f kOhm"%(Rext(55.5, 6.75e6)) )

#example from datasheet
print("%8.2f kOhm"%(Rext(55.5, 14e6)) )
