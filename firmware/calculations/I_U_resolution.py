# -*- coding: utf-8 -*-
"""
Calculate & evaluate the resolution influence of I and U
"""
import sys
sys.path.append("../../software")
sys.path.append("../../software/pyUSBtin")  # needed for OpenFlowMeter
from OpenFlowMeter import PT100
from OpenFlowMeter import convertVoltage, convertCurrent, I2LSB, U2LSB

import matplotlib.pyplot as plt
import numpy as np

def resolution(Ulsb, Ilsb, Ugain = 1, Igain = 1):
    """

    Parameters
    ----------
    Ulsb : int
        measured voltage in LSB.
    Ilsb : int
        measured current in LSB.
    Ugain : float, optional
        coltage gain. The default is 1.
    Igain : int, optional
        current gain. The default is 1.

    Returns
    -------
    U : float
        voltage in V.
    I : float
        current in A.
    R : float
        resistance in Ohm.
    sU : float
        size of 1 LSB in voltage.
    sI : float
        size of 1 LSB in current.
    sR : float
        size of 1 LSB in resistance. Derived via gaussian error propagation
        from sU and sI.

    """

    U = convertVoltage(Ulsb) / Ugain
    I = convertCurrent(Ilsb) / Igain
    R = U / I

    # uncertaincy of voltage and current
    # 1 LSB
    sU = convertVoltage(1) / Ugain
    sI = convertCurrent(1) / Igain

    """
        R = U / I
        sR = sqrt( (dR/dU)**2 * sU**2 + (dR/dI)**2 * sI**2 )

        dR/dU = 1/I
        dR/dI = -U * 1/I**2
    """
    sR =  (1/I)**2  * sU**2 # voltage
    sR += U**2/I**4 * sI**2 # current

    sR = np.sqrt(sR)

    return U, I, R, sU, sI, sR


if __name__ == "__main__":

    """
    R2 =
        27k - 3.07
        22k - 3.54
        18k - 4.11
        12k - 5.66
        10k - 6.60
        5k6 - 11

        R1 = 56k
    """



    fig, ax = plt.subplots(2, 1, figsize=(6,10))

    d_sR  = np.array([])
    d_sR1 = np.array([])

    used_Igain = np.array([])
    used_Ugain = np.array([])


    T_PT100 = 40    # temperature of the PT100 sensor
    R = PT100.convertPT100_R( T_PT100 )

    DEBUG_PRINT = False
    #DEBUG_PRINT = True
    if DEBUG_PRINT:
        a_Istim = np.linspace(1e-3, 3e-3, 10)
    else:
        a_Istim = np.linspace(1e-3, 30e-3, 1000)

    a_max_Ugain = convertVoltage(4020) / (R * a_Istim)
    a_max_Igain = convertCurrent(4020) / a_Istim

    for Istim in a_Istim:

        # use here only 4020 LSB as fullscale, to prevent saturation
        max_Ugain = convertVoltage(4020) / (R * Istim)
        max_Igain = convertCurrent(4020) / Istim

        if DEBUG_PRINT:
            print("I stimulus: %4.2f mA"%(Istim*1000))
            print("max Gain: U: %4.2f V/V  I: %4.2f A/A"%(max_Ugain, max_Igain))
            print()

        # calculate the best matching gain
        # limit the gain to unity
        Ugain = 6
        Igain = 11

        Isat = False
        Usat = False

        Ilsb = I2LSB( Istim * Igain )
        if Ilsb > 4020:     # if High Gain is saturating use low gain
            Ilsb = I2LSB(Istim)
            Igain = 1
            Isat = True

        Ulsb = U2LSB( R * Istim * Ugain)
        if Ulsb > 4020:     # if High Gain is saturating use low gain
            Ulsb = U2LSB( R*Istim )
            Ugain = 1
            Usat = True

        #if Isat and Usat:   # if both are in saturation, skip it
        #    break

        used_Igain = np.append(used_Igain, Igain)
        used_Ugain = np.append(used_Ugain, Ugain)

        if DEBUG_PRINT:
            if Isat:
                print("I saturated")

            if Usat:
                print("U saturated")

        fs_U = convertVoltage(4095) / Ugain
        fs_I = convertCurrent(4095) / Igain
        fs_R = fs_U / fs_I

        if DEBUG_PRINT:
            print("Fullscale: %3.2f V \t %4.2f mA"%(fs_U, fs_I*1000))
            print("%5.2f Ohm = %5.2f °C"%(fs_R, PT100.convertPT100_T(fs_R)))

        U, I, R, sU, sI, sR = resolution(Ulsb, Ilsb, Ugain, Igain)
        d_sR = np.append(d_sR, sR)

        U, I, R, sU, sI, sR = resolution(U2LSB(R * Istim), I2LSB(Istim), 1, 1)
        d_sR1 = np.append(d_sR1, sR)

        if DEBUG_PRINT:
            print("%6.4f +- %5.4f V"%(U, sU), end="\t")
            print("%7.4f +- %5.4f mA"%(I*1000, sI*1000), end="\t")
            print("%2d - %2d"%(Ugain, Igain))
            print("%7.4f +- %6.4f Ohm"%(R, sR), end="\t")

            # add 100 to sR, because we are interested in the deltaT to 0°C
            print("+- %6.4f °C"%(PT100.convertPT100_T(100+sR) ))

            print("%7.4f %% %7.4f %% %7.4f %% %7.4f %%"%(
                sU/U*100, sI/I*100, sR/R*100,
                PT100.convertPT100_T(100+sR) / PT100.convertPT100_T(R) * 100
                ))

            print()
            print( '#'*40 )

    ax[0].plot(a_Istim*1000, a_max_Igain, label="maximal gain I", color="red")
    ax[0].plot(a_Istim*1000, a_max_Ugain, label="maximal gain U", color="green")

    ax[0].axhline(1, color="black", label="unity gain")
    ax[0].legend()

    ax[0].set_ylabel("gain")
    ax[0].set_xlabel("exitation current / mA")

    ax0 = ax[0].twinx()
    ax0.plot(a_Istim*1000, PT100.convertPT100_T(100+d_sR1), label="sigma R unity gain")
    ax0.set_ylabel("unity gain temperature resolution / K")

    ax[1].plot(a_Istim*1000, PT100.convertPT100_T(100+d_sR), label="sigma R")
    ax[1].set_ylabel("temperature resolution / K")
    ax[1].set_xlabel("exitation current / mA")

    ax1 = ax[1].twinx()

    ax1.plot(a_Istim*1000, used_Igain, color="red", label="used gain I")
    ax1.plot(a_Istim*1000, used_Ugain, color="green", label="used gain U")

    ax1.set_ylabel("gain (V/V or A/A)")

    """
    zi = Z.reshape( (len(uniX), len(uniY)) ).T

    # Create the contour plot
    CS = plt.contourf(xi, yi, zi,
                      128,   # number of levels
                      #cmap=plt.cm.rainbow
                      #cmap=plt.cm.plasma
                      cmap=plt.cm.viridis
                      )
    cbar = plt.colorbar()
    cbar.set_label('bias voltage / V')
    """
    fig.tight_layout()
    plt.show()