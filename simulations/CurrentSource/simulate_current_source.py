# -*- coding: utf-8 -*-
"""

"""
import os
import sys
sys.path.append("../PyLTSpice/")

# import partial for tweaking callback
from functools import partial


#from PyLTSpice import LTSpiceBatch, LTSteps, LTSpice_RawRead
from PyLTSpice import SimCommander, LTSteps, RawRead

def processing_data(raw_filename, log_file, Uset):
    print("Handling the simulation data of %s, log file %s" % (raw_filename, log_file))
    LTR = RawRead(raw_filename)
    # print all stored traces
    print(LTR.get_trace_names())

    # print simulation properties
    print(LTR.get_raw_property())

    current_measure = LTR.get_trace("V(current_measure)").get_wave(0)
    voltage_measure = LTR.get_trace("V(voltage_measure)").get_wave(0)


# select spice model

LTC = SimCommander("./current_source_mod_v1.asc")
LTC.set_parameters(temp=40)

# set default arguments
#LTC.set_parameters(res=0, cap=100e-6)
#LTC.set_component_value('R2', '2k')
#LTC.set_component_value('R1', '4k')
#LTC.set_element_model('V3', "SINE(0 1 3k 0 0 0)")
# define simulation
#LTC.add_instructions(
#    "; Simulation settings",
#    ".param run = 0"
#)

#for opamp in ('AD712', 'AD820'):
#    LTC.set_element_model('XU1', opamp)
#    for supply_voltage in (5, 10, 15):
#        LTC.set_component_value('V1', supply_voltage)
#        LTC.set_component_value('V2', -supply_voltage)
#        # overriding he automatic netlist naming
#        run_netlist_file = "{}_{}_{}.net".format(LTC.circuit_radic, opamp, supply_voltage)

#LTC.run(run_filename=run_netlist_file, callback=processing_data)


#LTC.reset_netlist()
#LTC.add_instructions(
#    "; Simulation settings",
#    ".ac dec 30 10 1Meg",
#    ".meas AC Gain MAX mag(V(out)) ; find the peak response and call it ""Gain""",
#    ".meas AC Fcut TRIG mag(V(out))=Gain/sqrt(2) FALL=last"
#)

LTC.run(callback=partial(processing_data, Uset=None))
LTC.wait_completion()

# Sim Statistics
print('Successful/Total Simulations: ' + str(LTC.okSim) + '/' + str(LTC.runno))