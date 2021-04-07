EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 3 7
Title "Open Flow Meter"
Date "2021-03-30"
Rev "1"
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
Text HLabel 7050 3300 2    50   Output ~ 0
Uout
Wire Wire Line
	7050 3300 5800 3300
$Comp
L Analog_DAC:MCP4725xxx-xCH U3
U 1 1 60651218
P 5400 3300
AR Path="/60624FF4/60651218" Ref="U3"  Part="1" 
AR Path="/606570C9/60651218" Ref="U5"  Part="1" 
F 0 "U5" H 5400 3781 50  0000 C CNN
F 1 "MCP4725xxx-xCH" H 5400 3690 50  0000 C CNN
F 2 "Package_TO_SOT_SMD:SOT-23-6" H 5400 3050 50  0001 C CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/22039d.pdf" H 5400 3300 50  0001 C CNN
	1    5400 3300
	1    0    0    -1  
$EndComp
Wire Wire Line
	5000 3200 4400 3200
Wire Wire Line
	5000 3300 4400 3300
Text Label 4500 3200 0    50   ~ 0
SCL
Text Label 4500 3300 0    50   ~ 0
SDA
Text HLabel 4400 3200 0    50   Input ~ 0
SCL
Text HLabel 4400 3300 0    50   BiDi ~ 0
SDA
$EndSCHEMATC
