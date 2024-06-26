# OpenFlowMeter
## Purpose
Measuring flow of gases and maybe liquids. 

## Principle
Measures the volume flow by the amount of heat transferred to a gas flow. This can be either done by constantly heating the sensor or by evaluating temperature cycles.

# Hardware
The hardware is based around two voltage controlled current sources, which are controlled and readout via a STM32F103 microcontroller. 
The controller provides the ADCs for reading the voltages and current as well as the digital communication to the outside of the PCB.

## Photographs of the populated PCB
<img width="90%" src="images/photographs/OFMv2.0_TOP.jpg" alt="Picture of the PCB from TOP side">

<img width="90%" src="images/photographs/OFMv2.0_BOT.jpg" alt="Picture of the PCB from BOT side">

# References
The working principle of this device is adapted from a proposal of the LHC gas group at CERN. In addition there is a report of a student, explaining / proposing this technique more in detail.

[1] [M. van der Klis. PT100 channel flow meter for the LHC experiments, Technical Student Report Feb. 2001](https://cernbox.cern.ch/s/Kf3zl0SAsNUGON4)

[2] [F.Hahn, S.Haider, M. v.d. Klis, C. Zinoni, Proposal for a gas flow meter at LHC, 10.2.2001](https://cernbox.cern.ch/s/3Rpv9e0gEgKwOim)

# PCBs
PCBs are available from AISLER https://aisler.net/p/MVHMBVKT
