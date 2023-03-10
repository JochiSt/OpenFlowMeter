# -*- coding: utf-8 -*-
"""

"""
import matplotlib.pyplot as plt
import numpy as np

from simulate_OFM import SimADC

def PWM2Voltage(PWM):
    return 3.3 * PWM / 4096

def getVoltageBeforeAmplifier(UADC, Uoffset, R1=56e3, R2=5.6e3):
    return (R1 * Uoffset + R2 * UADC)/(R1 + R2)

def LSB2U(LSB):
    return LSB / 4096 * 3.3

def U2I(U):
    """
        converts measured OFM current voltage into mA
    """
    return U * 10e-3 * 1000

def analyse_OFMfull(filename):
    if not filename:
        return

    npzfile = np.load(filename)

    result_PWM_I   = npzfile['result_PWM_I'].astype(float)
    result_PWM_B   = npzfile['result_PWM_B'].astype(float)
    result_uadc_in = npzfile['result_uadc_in']
    result_iadc_in = npzfile['result_iadc_in']
    result_uswitch = npzfile['result_uswitch']

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
        ax[i].plot(
            result_PWM_I[switch_pos[i]][index],
            result_uadc_in[switch_pos[i]][index],
            label="UADC in",
            color=color
            )

        ax[i].plot(
            result_PWM_I[switch_pos[i]][index],
            result_iadc_in[switch_pos[i]][index],
            label="IADC in",
            linestyle='--',
            color=color,
            )

        ax[i].plot(
            result_PWM_I[switch_pos[i]][index],
            result_uswitch[switch_pos[i]][index],
            color=color,
            linestyle='dotted',
            label="switch voltage"
            )

    for i in [0,1]:
        ax[i].set_xlabel("current PWM setting / LSB")

    ax2 = [
        ax[0].twinx(),
        ax[1].twinx()
        ]

    color = 'green'
    for i in [0,1]:
        ax2[i].set_ylabel("raw values / LSB", color=color)
        ax2[i].spines['right'].set_position(('outward', 0))
        ax2[i].tick_params(axis='y', labelcolor=color)
        #ax2[i].set_yscale('log', base=2)

        ax2[i].plot(
            result_PWM_I[switch_pos[i]][index],
            result_uadc[switch_pos[i]][index],
            label="UADC",
            color=color)

        ax2[i].plot(
            result_PWM_I[switch_pos[i]][index],
            result_iadc[switch_pos[i]][index],
            label="IADC",
            linestyle='--',
            color=color)

        ax2[i].plot(
            result_PWM_I[switch_pos[i]][index],
            result_PWM_B[switch_pos[i]][index],
            label="bias PWM",
            linestyle='-',
            color=color)

    ax3 = [
        ax[0].twinx(),
        ax[1].twinx()
        ]


    color = 'orange'
    for i in [0,1]:
        ax3[i].set_ylabel("voltage before amplifier / V", color=color)
        ax3[i].spines['right'].set_position(('outward', 55))
        ax3[i].tick_params(axis='y', labelcolor=color)

        if i == 1:
            ax3[i].plot(
                result_PWM_I[switch_pos[i]][index],
                getVoltageBeforeAmplifier(
                    LSB2U(result_uadc[switch_pos[i]][index]),
                    PWM2Voltage(result_PWM_B[switch_pos[i]][index])),
                color=color,
                label="voltage before amplifier")
        else:
            ax3[i].plot(
                result_PWM_I[switch_pos[i]][index],
                LSB2U(result_uadc[switch_pos[i]][index]),
                color=color,
                label="voltage before amplifier")

    ###########################################################################

    ax4 = [
        ax[0].twinx(),
        ax[1].twinx()
        ]

    color = 'red'
    for i in [0,1]:
        ax4[i].set_ylabel("current / mA", color=color)
        ax4[i].spines['right'].set_position(('outward', 55+55))
        ax4[i].tick_params(axis='y', labelcolor=color)

        if i == 1:
            ax4[i].plot(
                result_PWM_I[switch_pos[i]][index],
                U2I(getVoltageBeforeAmplifier(
                    LSB2U(result_uadc[switch_pos[i]][index]),
                    PWM2Voltage(result_PWM_B[switch_pos[i]][index]))),
                color=color,
                label="current before amplifier")
        else:
            ax4[i].plot(
                result_PWM_I[switch_pos[i]][index],
                U2I(LSB2U(result_uadc[switch_pos[i]][index])),
                color=color,
                label="current before amplifier")

    ax5 = [
        ax[0].twinx(),
        ax[1].twinx()
        ]

    color = 'black'
    for i in [0,1]:
        ax5[i].set_ylabel("resistance / Ohm", color=color)
        ax5[i].spines['right'].set_position(('outward', 55+55+40))
        ax5[i].tick_params(axis='y', labelcolor=color)

        if i == 1:
            ax5[i].plot(
                result_PWM_I[switch_pos[i]][index],

                getVoltageBeforeAmplifier(
                    LSB2U(result_uadc[switch_pos[i]][index]),
                    PWM2Voltage(result_PWM_B[switch_pos[i]][index]))
                /
                U2I(getVoltageBeforeAmplifier(
                    LSB2U(result_iadc[switch_pos[i]][index]),
                    PWM2Voltage(result_PWM_B[switch_pos[i]][index])))*1000
                ,
                color=color,
                label="current before amplifier")
        else:
            ax5[i].plot(
                result_PWM_I[switch_pos[i]][index],
                LSB2U(result_uadc[switch_pos[i]][index])/
                U2I(LSB2U(result_iadc[switch_pos[i]][index]))*1000,
                color=color,
                label="current before amplifier")

    for i in[0,1]:
        ax[i].legend()

    fig.tight_layout()
    plt.show()

if __name__ == "__main__":
    analyse_OFMfull('OFMfull_20230310_142123.npz')