# -*- coding: utf-8 -*-
"""

"""
import os
import sys

from functools import partial # import partial for tweaking callback
import numpy as np

sys.path.append("../PyLTSpice/")
from PyLTSpice import SimCommander, LTSteps, RawRead

sys.path.append("../../software/")
sys.path.append("../../software/pyUSBtin")
from OpenFlowMeter import PT100

def processing_data(raw_filename, log_file, Uset):
    print("Handling the simulation data of %s, log file %s" % (raw_filename, log_file))
    LTR = RawRead(raw_filename)
    # print all stored traces
    #print(LTR.get_trace_names())

    # print simulation properties
    #print(LTR.get_raw_property())

    current_setpoint= np.mean(LTR.get_trace("V(current_setpoint)").get_wave(0))

    current_pt100   = np.mean(LTR.get_trace("I(PT100)").get_wave(0))*1000

    current_measure = np.mean(LTR.get_trace("V(current_measure)").get_wave(0))
    voltage_measure = np.mean(LTR.get_trace("V(voltage_measure)").get_wave(0))

    print(current_setpoint)
    print(current_pt100)
    print(current_measure)
    print(voltage_measure)

    R_PT100 = voltage_measure / (current_measure * 10 / 1000)
    print("R_PT100: ", R_PT100)
    print("Temperature", PT100.convertPT100_T(R_PT100))


# select spice model

LTC = SimCommander("./current_source_mod_v1.asc")
LTC.set_parameters(temp=40)

LTC.wait_completion()

# Sim Statistics
print('Successful/Total Simulations: ' + str(LTC.okSim) + '/' + str(LTC.runno))