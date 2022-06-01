# -*- coding: utf-8 -*-

import math

TS = 55.5
Fadc = 6.75e6
Cadc = 8e-12
Nbits = 12
Radc = 1e3

RAIN = TS / (Fadc * Cadc * math.log (math.pow(2, Nbits+2)) ) - Radc
print("%8.2f kOhm"%(RAIN/1000) )

#example from datasheet
TS = 55.5
Fadc = 14e6

RAIN = TS / (Fadc * Cadc * math.log (math.pow(2, Nbits+2)) ) - Radc
print("%8.2f kOhm"%(RAIN/1000) )
