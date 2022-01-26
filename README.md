# OpenFlowMeter
## Purpose
Measuring flow of gases and maybe liquids. 

## Principle
Measures the volume flow by the amount of heat transferred to a gas flow.


# References
The working principle of this device is adapted from a proposal of the LHC gas group at CERN. In addition there is a report of a student, explaining / proposing this technique more in detail.

[1] M. van der Klis. PT100 Channel Flowmeter for the LHC Experiments, Technical Student Report Feb. 2001


# PCBs
PCBs are available from AISLER https://aisler.net/p/MVHMBVKT

## SmartTest Error
When AISLER is doing their SmartTest, the following error is reported.
![](https://github.com/JochiSt/OpenFlowMeter/blob/db96e790106f075d02dbe3f1536355f5300a0a81/images/aisler/SmartTestResult.PNG)

This error is fine, because the jumper 

![](https://github.com/JochiSt/OpenFlowMeter/blob/db96e790106f075d02dbe3f1536355f5300a0a81/images/aisler/EEPROM_jumper.PNG) is closed on default connecting pin 7 of the EEPROM to GND.
