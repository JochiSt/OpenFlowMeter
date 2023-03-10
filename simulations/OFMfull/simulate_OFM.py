# -*- coding: utf-8 -*-
"""

"""
import os
import sys

from functools import partial, update_wrapper # import partial for tweaking callback
import numpy as np

import pprint
import time

sys.path.append("../PyLTSpice/")
from PyLTSpice import SimCommander, LTSteps, RawRead

sys.path.append("../../software/")
sys.path.append("../../software/pyUSBtin")
from OpenFlowMeter import PT100

def SimADC(Uin = 0, Uref = 3.3):
    LSBs = Uin / Uref * 4096
    return int(np.round(LSBs))

result_PWM_I = np.array([])
result_PWM_B = np.array([])
result_uadc_in = np.array([])
result_iadc_in = np.array([])
result_uswitch = np.array([])

def processing_data(raw_filename, log_file, PWMI, PWMB):
    print("Handling the simulation data of %s, log file %s" % (raw_filename, log_file))
    LTR = RawRead(raw_filename)

    # print simulation properties
    #pprint.pprint(LTR.get_raw_property())

    global result_PWM_I
    global result_PWM_B
    global result_uadc_in
    global result_iadc_in
    global result_uswitch

    print("PWM I", PWMI)
    print("PWM B", PWMB)

    steps = LTR.get_steps()
    for step in range(len(steps)):

        print("Steps", steps[step])

        uswitch = np.mean(LTR.get_trace("V(switch)").get_wave(step)[:-10])

        uadc_in = np.mean(LTR.get_trace("V(uadc)").get_wave(step)[:-10])
        iadc_in = np.mean(LTR.get_trace("V(iadc)").get_wave(step)[:-10])

        uadc = SimADC(uadc_in)
        iadc = SimADC(iadc_in)

        print(uswitch)
        print(uadc_in, iadc_in)
        print(uadc, iadc)

        result_PWM_I = np.append(result_PWM_I, PWMI)
        result_PWM_B = np.append(result_PWM_B, PWMB)

        result_uadc_in =  np.append(result_uadc_in, uadc_in)
        result_iadc_in =  np.append(result_iadc_in, iadc_in)
        result_uswitch =  np.append(result_uswitch, uswitch)


###############################################################################

# select spice model
LTC = SimCommander(
    "./OFMfull.asc",
    parallel_sims=2             # limit number of parallel simulations)
    )
LTC.set_parameters(temp=40)


for pwm_set_i in [ 10, 1024, 2048, 4096]:

    LTC.set_parameter('CCR_I', pwm_set_i)
    LTC.set_parameter('CCR_B', pwm_set_i)

    PWMI = LTC.get_parameter('CCR_I')
    PWMB = LTC.get_parameter('CCR_B')

    sim_callback = partial(processing_data, PWMI=PWMI, PWMB=PWMB)
    update_wrapper(sim_callback, processing_data)
    LTC.run(callback=sim_callback)

LTC.wait_completion()
# Sim Statistics
print('Successful/Total Simulations: ' + str(LTC.okSim) + '/' + str(LTC.runno))


# save results in numpy file format
np.savez("OFMfull_%s.npz"%(time.strftime("%Y%m%d_%H%M%S")),
         result_PWM_I   = result_PWM_I,
         result_PWM_B   = result_PWM_B,
         result_uadc_in = result_uadc_in,
         result_iadc_in = result_iadc_in,
         result_uswitch = result_uswitch,
         )