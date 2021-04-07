EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 5 7
Title "Open Flow Meter"
Date "2021-03-30"
Rev "1"
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Analog_ADC:ADS1115IDGS U4
U 1 1 6062EF45
P 4000 3500
F 0 "U4" H 4000 4181 50  0000 C CNN
F 1 "ADS1115IDGS" H 4000 4090 50  0000 C CNN
F 2 "Package_SO:TSSOP-10_3x3mm_P0.5mm" H 4000 3000 50  0001 C CNN
F 3 "http://www.ti.com/lit/ds/symlink/ads1113.pdf" H 3950 2600 50  0001 C CNN
	1    4000 3500
	-1   0    0    -1  
$EndComp
Wire Wire Line
	4400 3400 5250 3400
Wire Wire Line
	5250 3500 4400 3500
Wire Wire Line
	5250 3600 4400 3600
Wire Wire Line
	5250 3700 4400 3700
Text HLabel 5250 3400 2    50   Input ~ 0
IN0
Text HLabel 5250 3500 2    50   Input ~ 0
IN1
Text HLabel 5250 3600 2    50   Input ~ 0
IN2
Text HLabel 5250 3700 2    50   Input ~ 0
IN3
Wire Wire Line
	3600 3500 3000 3500
Wire Wire Line
	3600 3600 3000 3600
Text Label 3100 3500 0    50   ~ 0
SCL
Text Label 3100 3600 0    50   ~ 0
SDA
$Comp
L power:GND #PWR010
U 1 1 6064A32D
P 4000 3950
F 0 "#PWR010" H 4000 3700 50  0001 C CNN
F 1 "GND" H 4005 3777 50  0000 C CNN
F 2 "" H 4000 3950 50  0001 C CNN
F 3 "" H 4000 3950 50  0001 C CNN
	1    4000 3950
	1    0    0    -1  
$EndComp
Wire Wire Line
	4000 3950 4000 3900
Text HLabel 3000 3500 0    50   Input ~ 0
SCL
Text HLabel 3000 3600 0    50   BiDi ~ 0
SDA
$EndSCHEMATC
