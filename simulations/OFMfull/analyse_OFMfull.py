# -*- coding: utf-8 -*-
"""

"""
import matplotlib.pyplot as plt
import numpy as np

from simulate_OFM import SimADC

def analyse_OFMfull(filename):
    if not filename:
        return

    npzfile = np.load(filename)

    result_PWM_I   = npzfile['result_PWM_I'].astype(float)
    result_PWM_B   = npzfile['result_PWM_B'].astype(float)
    result_uadc_in = npzfile['result_uadc_in']
    result_iadc_in = npzfile['result_iadc_in']
    result_uswitch = npzfile['result_uswitch']

    print(result_uadc_in)

    result_uadc = SimADC(result_uadc_in)
    result_iadc = SimADC(result_iadc_in)


    fig, ax = plt.subplots(2, 1, figsize=(8,10))

    switch_off = np.where(result_uswitch < 1.0 )
    switch_on  = np.where(result_uswitch > 1.0 )

    switch_pos = [switch_off, switch_on]

    ###########################################################################
    # PWM
    color = 'tab:blue'
    for i in [0,1]:
        ax[i].set_ylabel("ADC input voltage", color=color)
        ax[i].tick_params(axis='y', labelcolor=color)

        index = np.argsort(result_PWM_I[switch_pos[i]])
        ax[i].plot( result_PWM_I[switch_pos[i]][index], result_uadc_in[switch_pos[i]][index], label="UADC in")
        ax[i].plot( result_PWM_I[switch_pos[i]][index], result_iadc_in[switch_pos[i]][index], label="IADC in")

        ax[i].plot( result_PWM_I[switch_pos[i]][index], result_uswitch[switch_pos[i]][index], label="switch voltage")

    #for i in [0,1]:
        #ax[i].plot( timestamp, temperatures[i], label="calc. T", color='deeppink', linewidth=1)

    for i in[0,1]:
        ax[i].legend()

if __name__ == "__main__":
    analyse_OFMfull('OFMfull_20230310_121316.npz')