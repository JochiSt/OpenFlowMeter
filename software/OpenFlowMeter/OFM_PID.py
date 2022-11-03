# -*- coding: utf-8 -*-
"""
Created on Sun Mar 13 07:08:06 2022

@author: steinmann

original from:
    htps://itzwieseltal.wordpress.com/2020/06/02/python-pid-regler/
    but heavily modify to meet the requirements of the OFM
"""

class OFM_PID(object) :

    def __init__(self, dt, max, min, kp, kd, ki) :
        self.dt  = dt
        self.max = max
        self.min = min
        self.kp  = kp
        self.kd  = kd
        self.ki  = ki
        self.int = 0
        self.err = 0

    def run(self, setpoint, actual) :
        # calculate error
        error = setpoint - actual

        # proportional part
        P = self.kp * error

        # integral part
        self.int += error * self.dt
        I = self.ki * self.int

        #differential part
        D = self.kd * (error - self.err) / self.dt
        self.err = error

        # sum all together for the output
        output = P + I + D

        # limit output to be between min and max
        if output > self.max:
            output = self.max
        elif output < self.min:
            output = self.min

        return(output);


if __name__ == "__main__":
    # small test
    pid = OFM_PID(dt=0.5, max=100, min=-100, kp=0.1, kd=0.00, ki=0.5)

    val = 20;
    for i in range(100):
        inc = pid.run(50, val)
        print('val:','{:7.3f}'.format(val),' inc:','{:7.3f}'.format(inc) )
        val += inc
