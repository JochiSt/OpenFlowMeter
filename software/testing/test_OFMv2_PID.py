# -*- coding: utf-8 -*-

import sys
sys.path.append("../")
from OpenFlowMeter import OpenFlowMeter
from CANsetup import CANsetup

from plot_OFMv2_PID import plot_OFMv2_PID

import numpy as np

import time

OFM_ADC_MIN = 40

def main():
    setup = None
    filename = None

    try:
        print("Getting the configuration from OFM")
        print('#'*70+'\n')

        # initialise USBtin
        setup = CANsetup()

        # initialise OFM
        ofm =  OpenFlowMeter(usbtin = setup.usbtin, boardID=0x1)
        ofm.requestConfigFromDevice()
        time.sleep(2)
        ofm.requestConfigFromDevice()
        time.sleep(2)
        ofm.requestConfigFromDevice()
        time.sleep(2)

        ofm.config.interval_I2C_TMP100 = 64

        ofm.config.PID_flags = 0b00000000

        # PID settings channel 0
        ofm.config.PID_T[0] = 40.0
        ofm.config.PID_P[0] = 0
        ofm.config.PID_I[0] = 0
        ofm.config.PID_D[0] = 0

        # PID settings channel 1
        ofm.config.PID_T[1] = 30.0
        ofm.config.PID_P[1] = 8
        ofm.config.PID_I[1] = 0
        ofm.config.PID_D[1] = 0

        time.sleep(1)
        ofm.changeConfig()
        time.sleep(1)

        print('\n'+'#'*70+'\n')

        ofm.requestConfigFromDevice()
        time.sleep(1)
        ofm.config.printout()

        ofm.setDAC(OFM_ADC_MIN, OFM_ADC_MIN)
        time.sleep(2)

        time0 = time.time()
        timestamp = np.array([])

        t_tmp100 = np.array([])
        dac  = [np.array([]), np.array([])]
        setp = [np.array([]), np.array([])]
        temperatures = [np.array([]), np.array([])]
        voltages = [np.array([]), np.array([])]
        currents = [np.array([]), np.array([])]
        gains = np.array([])

        current_raw = [
            [np.array([]), np.array([])],
            [np.array([]), np.array([])]
            ]

        voltage_raw = [
            [np.array([]), np.array([])],
            [np.array([]), np.array([])]
            ]

        print("Use CTRL-C to stop datataking...")

        dac_on = False

        TIME_START = 30
        TIME_PID_ACTIVE = 600
        TIME_DISTURB = 500
        TIME_STOP = 60

        # for debugging
        #TIME_START = 2
        #TIME_PID_ACTIVE = 10
        #TIME_STOP = 2

        disturbed = False

        events = []

        try:
            while True:
                ofm.waitForNewMessage()
                ofm.hasNewMessage = False

                runtime = time.time()-time0

                if runtime > TIME_START and runtime < TIME_START + TIME_PID_ACTIVE  and not dac_on:
                    dac_on = True
                    ofm.config.PID_active[1] = True
                    ofm.changeConfig()
                    print("PID enabled")
                    events.append( (runtime, "PID enabled") )

                if runtime > TIME_START + TIME_PID_ACTIVE and dac_on:
                    dac_on = False
                    ofm.config.PID_active[1] = False
                    ofm.changeConfig()
                    print("PID disabled")
                    events.append( (runtime, "PID disabled") )
                    ofm.setDAC(OFM_ADC_MIN, OFM_ADC_MIN)

                if runtime > TIME_START + TIME_PID_ACTIVE + TIME_STOP:
                    break

                if runtime > TIME_START + TIME_DISTURB and not disturbed:
                    print("Changing setpoint of PID")
                    disturbed = True
                    ofm.config.PID_T[1] = ofm.config.PID_T[1] + 10
                    ofm.changeConfig()
                    events.append( (runtime, "PID setpoint %3.1f"%(ofm.config.PID_T[1])) )


                # recording of the data

                timestamp = np.append(timestamp, runtime)
                t_tmp100 = np.append(t_tmp100, ofm.TMP100_T)
                gains = np.append(gains, ofm.ADCgains)

                for ch in [0,1]:
                    dac[ch]  = np.append(dac[ch], ofm.DACreadback[ch])
                    setp[ch] = np.append(setp[ch], ofm.config.PID_T[ch])
                    temperatures[ch] = np.append(temperatures[ch], ofm.temperatures[ch])

                    voltages[ch] = np.append(voltages[ch], ofm.voltages[ch])
                    currents[ch] = np.append(currents[ch], ofm.currents[ch])

                    for gain in [0,1]:
                        voltage_raw[ch][gain] = np.append(
                                voltage_raw[ch][gain],
                                ofm.voltage(ch, gain)
                            )

                        current_raw[ch][gain] = np.append(
                                current_raw[ch][gain],
                                ofm.current(ch, gain)
                            )

        except KeyboardInterrupt:
            pass

        except Exception as e:
            print(e)

        filename = "PIDtest_%s.npz"%(time.strftime("%Y%m%d_%H%M%S"))
        np.savez(filename,
                    timestamp = timestamp,
                    temperatures = temperatures, setp=setp, dac=dac,
                    voltages = voltages, currents = currents,
                    current_raw = current_raw,
                    voltage_raw = voltage_raw,
                    events = events,
                    ofmcfg = ofm.config.toBytes(),
                    gains = gains
                    )

        ofm.setDAC(OFM_ADC_MIN, OFM_ADC_MIN)
        ofm.config.PID_flags = 0b00000000
        ofm.changeConfig()

    except Exception as e:
        print(e)
        pass

    finally:
        if setup:
            setup.deinit()

    return filename

if __name__ == "__main__":
    filename = main()
    plot_OFMv2_PID(filename)

