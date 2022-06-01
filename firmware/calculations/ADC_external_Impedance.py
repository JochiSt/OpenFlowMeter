# -*- coding: utf-8 -*-

import math

def Rext(TS, Fadc, Nbits=12):
    """
        returns the maximal allowed external impedance in kOhm
        see page 75 of https://www.st.com/resource/en/datasheet/stm32f103c8.pdf for details
    """

    print("TS = %4.1f cycles\tFadc = %6.2f MHz"%(TS, Fadc/1e6))
    Cadc = 8e-12
    Radc = 1e3
    RAIN = TS / (Fadc * Cadc * math.log (math.pow(2, Nbits+2)) ) - Radc
    return RAIN / 1000

print("#"*80)
print("Calculate the maximal allowed external impedance:")
print("\n")
print("Setup used in OpenFlowMeter")

print("%8.2f kOhm"%(Rext(55.5, 6.75e6)) )

print("\n")
print("#"*80)
print("Examples from datasheet:")
#example from datasheet
print("%8.2f kOhm"%(Rext( 1.5, 14e6)) )
print("%8.2f kOhm"%(Rext( 7.5, 14e6)) )
print("%8.2f kOhm"%(Rext(13.5, 14e6)) )
print("%8.2f kOhm"%(Rext(28.5, 14e6)) )
print("%8.2f kOhm"%(Rext(41.5, 14e6)) )
print("%8.2f kOhm"%(Rext(55.5, 14e6)) )
print("%8.2f kOhm"%(Rext(71.5, 14e6)) )
