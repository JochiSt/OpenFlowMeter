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
    gain : TYPE, optional
        DESCRIPTION. The default is 1.

    Returns
    -------


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

    Ugain=5
    Igain=5

    fig, ax = plt.subplots(2, 1, figsize=(6,10))

    d_sR = {}
    d_Ulsb = {}
    d_Ilsb = {}

    R = PT100.convertPT100_R(40)

    for Istim in [
             1e-3,
            10e-3,
            20e-3,
            30e-3,
            ]:
        for Ugain, Igain in [
                (1,1),
                (5,5),

                ]:

                if Istim not in d_sR.keys():
                    d_sR[Istim] = np.array([])
                    d_Ulsb[Istim] = np.array([])
                    d_Ilsb[Istim] = np.array([])

                Ilsb = I2LSB( Istim * Igain )
                if Ilsb > 4000:
                    Ilsb = I2LSB(Istim)
                    Igain = 1

                Ulsb = U2LSB( R * Istim * Ugain)
                if Ulsb > 4000:
                    Ulsb = U2LSB( R*Istim )
                    Ugain = 1

                U, I, R, sU, sI, sR = resolution(Ulsb, Ilsb, Ugain, Igain)

                d_sR[Istim] = np.append(d_sR[Istim], sR)
                d_Ulsb[Istim] = np.append(d_Ulsb[Istim], Ulsb)

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


    fig.tight_layout()
    plt.show()