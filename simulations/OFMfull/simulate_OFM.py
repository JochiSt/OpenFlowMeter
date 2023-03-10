# -*- coding: utf-8 -*-
"""

"""
import os
import sys

from functools import partial # import partial for tweaking callback
import numpy as np

import pprint

sys.path.append("../PyLTSpice/")
from PyLTSpice import SimCommander, LTSteps, RawRead

sys.path.append("../../software/")
sys.path.append("../../software/pyUSBtin")
from OpenFlowMeter import PT100

def SimADC(Uin = 0, Uref = 3.3):
    LSBs = Uin / Uref * 4096
    return int(np.round(LSBs))


def processing_data(raw_filename, log_file):
    print("Handling the simulation data of %s, log file %s" % (raw_filename, log_file))
    LTR = RawRead(raw_filename)
    # print all stored traces
    print("Traces:")
    for name in LTR.get_trace_names():
        print(name)
    print()

    # print simulation properties
    print(LTR.get_raw_property())
    pprint.pprint(LTR.get_raw_property())

    uadc_in = np.mean(LTR.get_trace("V(uadc)").get_wave(0)[:-10])
    iadc_in = np.mean(LTR.get_trace("V(iadc)").get_wave(0)[:-10])

    uadc = SimADC(uadc_in)
    iadc = SimADC(iadc_in)

    print(uadc_in, iadc_in)
    print(uadc, iadc)


# select spice model

LTC = SimCommander(
    "./OFMfull.asc",
    parallel_sims=2             # limit number of parallel simulations)
    )
LTC.set_parameters(temp=40)

#for Uset in [0.5, 1, 1.5, 2, 2.5, 3, 3.3]:
#    LTC.set_component_value('V3', Uset)

LTC.run(callback=processing_data)
LTC.wait_completion()

# Sim Statistics
print('Successful/Total Simulations: ' + str(LTC.okSim) + '/' + str(LTC.runno))