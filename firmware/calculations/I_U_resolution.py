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

from scipy.optimize import minimize

from eseries import find_nearest, E12

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


def calculate_Tresolution(Ugain, Igain, T_PT100 = 40):

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

    d_sR  = np.array([])
    used_Igain = np.array([])
    used_Ugain = np.array([])

    R = PT100.convertPT100_R( T_PT100 )

    DEBUG_PRINT = False
    #DEBUG_PRINT = True
    if DEBUG_PRINT:
        a_Istim = np.linspace(1e-3, 3e-3, 10)
    else:
        a_Istim = np.linspace(1e-3, 30e-3, 1024)

    a_max_Ugain = convertVoltage(4020) / (R * a_Istim)
    a_max_Igain = convertCurrent(4020) / a_Istim

    for Istim in a_Istim:

        if DEBUG_PRINT:
            print("I stimulus: %4.2f mA"%(Istim*1000))
            print()

        # calculate the best matching gain
        # limit the gain to unity
        #Ugain = 5
        #Igain = 11

        Isat = False
        Usat = False

        Ilsb = I2LSB( Istim * Igain )
        Ulsb = U2LSB( R * Istim * Ugain)

        if Ilsb > 4020:     # if High Gain is saturating use low gain
            Isat = True

        if Ulsb > 4020:     # if High Gain is saturating use low gain
            Usat = True

        """
        # this is what is currently implemented in the firmware
        if Isat or Usat:
            Isat = True
            Usat = True
        """

        if Isat:
            Ilsb = I2LSB(Istim)
            Igain = 1

        if Usat:
            Ulsb = U2LSB( R*Istim )
            Ugain = 1

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

    return a_Istim, d_sR, used_Igain, used_Ugain


def minfunc(gain):
    a_Istim, d_sR, used_Igain, used_Ugain = calculate_Tresolution(gain[0], gain[1])

    sT_raw = PT100.convertPT100_T( 100 + d_sR )

    # give the lower exitation currents a higher weighting
    sT = np.where(a_Istim < 3.0e-3, sT_raw * 10 , sT_raw)
    sT = np.where(a_Istim < 1.2e-3, sT_raw * 50 , sT)    # no self warming

    if np.max(sT_raw) >= 1:
        return np.sum(sT) * 100

    return np.sum(sT)
    #return np.max(sT)

if __name__ == "__main__":

    ###########################################################################
    # Optimise the best gain

    T_PT100 = 40

    Ugain = 3
    Igain = 20

    # minimize areas of temperature resolution, gives a compromise between
    # low and high current resolution.
    res = minimize( minfunc,
                   (Ugain, Igain),
                   bounds=[ (1, 11),(1, 11) ] ,
                   tol=1e-15,
                   #method='TNC',
                   method='SLSQP',
                   #method='L-BFGS-B',
                   options={'disp': False, 'maxiter': 500}
                   )
    if not res.success:
        print(res)

    Ugain = res.x[0]
    Igain = res.x[1]

    ###########################################################################
    # Calculate the resistors

    #  GAIN = 1 + R1/R2
    # R1 = (GAIN - 1) * R2
    # R2 = R1 / (GAIN - 1)
    R2 = 56e3

    # calculate the resistances from E12
    R1_U = (Ugain - 1) * R2
    R1_U = find_nearest(E12, R1_U)

    R1_I = (Igain - 1) * R2
    R1_I = find_nearest(E12, R1_I)

    # possible realisations
    Ugain_R = 1 + R1_U / R2
    Igain_R = 1 + R1_I / R2

    ###########################################################################
    # Plotting

    a_Istim,   d_sR,   used_Igain,   used_Ugain   = calculate_Tresolution(Ugain, Igain, T_PT100)
    a_Istim_R, d_sR_R, used_Igain_R, used_Ugain_R = calculate_Tresolution(Ugain_R, Igain_R, T_PT100)

    fig, ax = plt.subplots(1, 1, figsize=(6,5))
    fig.suptitle("Resolution for PT100 @ %3.1f °C"%(T_PT100))

    plts = []
    plts += ax.plot(a_Istim*1000, PT100.convertPT100_T(100+d_sR),
                        label="T resolution (max: %4.2f, avg: %4.2f)"%(
                                    np.max(  PT100.convertPT100_T( 100+d_sR )),
                                    np.mean( PT100.convertPT100_T( 100+d_sR ))
                                    )
                        )

    plts += ax.plot(a_Istim_R*1000, PT100.convertPT100_T(100+d_sR_R),
                        label="T resolution R (max: %4.2f, avg: %4.2f)"%(
                                    np.max(  PT100.convertPT100_T( 100+d_sR_R )),
                                    np.mean( PT100.convertPT100_T( 100+d_sR_R ))
                                    )
                        )

    ax.set_ylabel("temperature resolution / K")
    ax.set_xlabel("exitation current / mA")
    #ax.legend(loc='best')

    ax1 = ax.twinx()
    plts += ax1.plot(a_Istim*1000, used_Igain, color="darkred",
                         label="opt. gain I (%6.2f)"%(Igain))
    plts += ax1.plot(a_Istim*1000, used_Ugain, color="darkgreen",
                         label="opt. gain U (%6.2f)"%(Ugain))

    plts += ax1.plot(a_Istim_R*1000, used_Igain_R, color="red",
                         label="R gain I (%6.2f R1=%4.1f kOhm R2=%4.1f kOhm)"%(Igain_R, R1_I/1000, R2/1000))
    plts += ax1.plot(a_Istim_R*1000, used_Ugain_R, color="lightgreen",
                         label="R gain U (%6.2f R1=%4.1f kOhm R2=%4.1f kOhm)"%(Ugain_R, R1_U/1000, R2/1000))

    ax1.set_ylabel("gain (V/V or A/A)")

    labs = [l.get_label() for l in plts]
    ax.legend(plts, labs, loc=0)

    fig.tight_layout()
    plt.savefig("gain_optimisation.png")
    plt.show()