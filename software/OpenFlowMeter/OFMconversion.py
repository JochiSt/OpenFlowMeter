# -*- coding: utf-8 -*-

def convertCurrent(lsb, gain=0):
    current = lsb * 3.3/4095 * 10e-3
    if gain:
        current /= 1 + 470e3 / 56e3
    return current

def convertVoltage(lsb, gain=0):
    voltage = lsb * 3.3/4095
    if gain:
        voltage /= 1 + 330e3 / 56e3
    return voltage

def U2LSB(voltage):
    return int(round( voltage / 3.3 * 4095, 0 ))

def I2LSB(current):
    return int(round( current / 10e-3 / 3.3 * 4095 , 0))

class PT100(object):
    A = 3.9083e-3
    B = -5.775e-7
    C = -4.183e-12
    R0 = 100

    @staticmethod
    def convertPT100_T(resistance):
        """
            convert the resistance of a PT100 into its temperature
        """

        return (resistance - PT100.R0)/(PT100.R0*PT100.A)

    @staticmethod
    def convertPT100_R(temperature):
        """
            convert the temperature of a PT100 into its resistance
            according to https://www.omega.de/prodinfo/pt100-formel.html

            temperature in degrees celsius
        """

        if temperature >= 0:
            return PT100.R0 *  (1 + PT100.A * temperature + PT100.B * temperature**2)
        else:
            return PT100.R0 * (1 + PT100.A * temperature + PT100.B * temperature**2 + PT100.C  * (temperature - 100) * temperature**3)

if __name__ == "__main__":

    for Ulsb in [103, 104, 105]:
        for Ilsb in [109, 110, 111]:
            voltage = convertVoltage(Ulsb)
            print(voltage, "V", end="\t")
            current = convertCurrent(Ilsb)
            print(current * 1000, "mA", end="\t")
            resistance =  voltage / current
            print(resistance, "Ohm")

    print( PT100.convertPT100_T(100 + 1) )
    print(PT100.convertPT100_R(0))
    print(PT100.convertPT100_R(-5))
