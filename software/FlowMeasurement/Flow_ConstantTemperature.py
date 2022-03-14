# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 07:05:41 2022

@author: steinmann
"""
import sys
sys.path.append("../")
from OpenFlowMeter import OpenFlowMeter, OFM_PID, PT100, convertCurrent, convertVoltage

from CANsetup import CANsetup
import time
import numpy as np

from plot_Flow_ConstantTemperature import plot_Flow_ConstantTemperature

def Flow_ConstantTemprature():
    # initialise USBtin
    setup = CANsetup()

    # initialise OFM
    ofm =  OpenFlowMeter(usbtin = setup.usbtin, boardID=0x1)

    # initialise PID controller
    PID_KP = 2
    PID_KD = 0.2
    PID_KI = 0.9
    pid = OFM_PID(dt=0.5,
                  max=1000,     # maximal DAC setpoint
                  min=32,         # minimal DAC setpoint (below 32 no reliable measurement can be done)
                  kp=PID_KP,    # proportional term
                  kd=PID_KD,    # differential term
                  ki=PID_KI       # integral term
                  )

    # configuration
    channel = 1                  # channels, we want to control the temperature
    SETPOINT_T =  40        # PT100 temperature set point

    MINUTES_RUNTIME = 5 # run time of the measurement

    # arrays to store the infomration for later analysis
    log_time = np.array([])
    log_dac = np.array([])
    log_T = np.array([])

    log_current = np.array([])
    log_voltage = np.array([])

    t_start = time.time()
    t_end = t_start + 60 * MINUTES_RUNTIME

    # set DAC to get a reliable first measurement
    dac = 32
    if channel == 0:
        ofm.setDAC(0, dac)
    else:
        ofm.setDAC(dac, 0)

    time.sleep(1) # wait one second

    try:
        while time.time() < t_end:
            ofm.waitForNewMessage()

            # log the time since start
            runtime =  time.time() - t_start
            log_time = np.append(log_time, runtime )

            # get the readings from OFM
            ofm_current = ofm.current(channel)
            ofm_voltage = ofm.voltage(channel)
            print("%7d\t%5d\t%5d"%(runtime, ofm_current, ofm_voltage), end="", flush=True)

            # log the raw current and voltage values
            log_current = np.append(log_current, ofm_current)
            log_voltage = np.append(log_voltage, ofm_voltage)

            # convert into SI values
            ofm_current = convertCurrent(ofm_current)
            ofm_voltage = convertVoltage(ofm_voltage)

            # calculate resistance and get temperature
            resistance = ofm_voltage / ofm_current
            temperature = PT100.convertPT100_T(resistance)
            # log the temperature
            log_T = np.append(log_T, temperature)

            # derive DAC setpoint from PID regulator
            dac =int( pid.run( SETPOINT_T, temperature) )
            # log dac setpoint
            log_dac = np.append(log_dac, dac)

            print("\t%5.2f\t%5.2f\t%5d"%( resistance, temperature, dac), end="", flush=True)

            # send the setpoint to the OFM
            if channel == 0:
                ofm.setDAC(0, dac)
            else:
                ofm.setDAC(dac, 0)

            ofm.hasNewMessage = False
            print()
    except Exception as e:
        print(e)

    print("deinit")
    ofm.setDAC(0,0)
    setup.deinit()

    # save everything to a NPZ file
    filename = "Tregulation_%s_CH%d_%d_%4.3f_%4.3f_%4.3f.npz"%(
                        time.strftime("%Y%m%d_%H%M%S"), channel, SETPOINT_T,
                            PID_KP, PID_KD, PID_KI )
    np.savez( filename,
                        log_dac=log_dac,
                        log_time=log_time,
                        log_T=log_T,
                        log_current=log_current,
                        log_voltage=log_voltage
                        )

    plot_Flow_ConstantTemperature.plot_Flow_ConstantTempreature(filename)

if __name__ == "__main__":
    Flow_ConstantTemprature()

