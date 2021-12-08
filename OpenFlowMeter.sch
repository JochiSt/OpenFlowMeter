EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 5
Title "Open Flow Meter"
Date "2021-03-30"
Rev "1"
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Sheet
S 1950 2900 2150 500 
U 606200AB
F0 "Controller" 50
F1 "OpenFlowMeter_Controller.sch" 50
$EndSheet
$Sheet
S 7700 3000 1800 550 
U 6062503A
F0 "CurrentSource 1" 50
F1 "OpenFlowMeter_CurrentSource.sch" 50
F2 "ISET" I L 7700 3100 50 
F3 "IMEAS" O L 7700 3200 50 
F4 "UMEAS" O L 7700 3300 50 
$EndSheet
$Sheet
S 7700 4550 1800 550 
U 6065743C
F0 "Current Source 2" 50
F1 "OpenFlowMeter_CurrentSource.sch" 50
F2 "ISET" I L 7700 4650 50 
F3 "IMEAS" O L 7700 4750 50 
F4 "UMEAS" O L 7700 4850 50 
$EndSheet
Text Notes 1950 2650 0    118  ~ 24
Powered with 3V3
Text Notes 7700 2750 0    118  ~ 24
Powered with 24V
Text Notes 7050 6800 0    118  ~ 24
Two channel flow meter.
$Comp
L Mechanical:MountingHole_Pad H1
U 1 1 61B62926
P 5750 6700
F 0 "H1" H 5850 6703 50  0000 L CNN
F 1 "MountingHole_Pad" H 5850 6658 50  0001 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3_Pad_Via" H 5750 6700 50  0001 C CNN
F 3 "~" H 5750 6700 50  0001 C CNN
	1    5750 6700
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole_Pad H2
U 1 1 61B6647F
P 6050 6700
F 0 "H2" H 6150 6703 50  0000 L CNN
F 1 "MountingHole_Pad" H 6150 6658 50  0001 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3_Pad_Via" H 6050 6700 50  0001 C CNN
F 3 "~" H 6050 6700 50  0001 C CNN
	1    6050 6700
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole_Pad H3
U 1 1 61B66B14
P 6350 6700
F 0 "H3" H 6450 6703 50  0000 L CNN
F 1 "MountingHole_Pad" H 6450 6658 50  0001 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3_Pad_Via" H 6350 6700 50  0001 C CNN
F 3 "~" H 6350 6700 50  0001 C CNN
	1    6350 6700
	1    0    0    -1  
$EndComp
$Comp
L Mechanical:MountingHole_Pad H4
U 1 1 61B6715E
P 6650 6700
F 0 "H4" H 6750 6703 50  0000 L CNN
F 1 "MountingHole_Pad" H 6750 6658 50  0001 L CNN
F 2 "MountingHole:MountingHole_3.2mm_M3_Pad_Via" H 6650 6700 50  0001 C CNN
F 3 "~" H 6650 6700 50  0001 C CNN
	1    6650 6700
	1    0    0    -1  
$EndComp
Wire Wire Line
	5750 6800 5750 6900
$Comp
L power:GND #PWR?
U 1 1 61B6C0DB
P 5750 6900
AR Path="/6062503A/61B6C0DB" Ref="#PWR?"  Part="1" 
AR Path="/6065743C/61B6C0DB" Ref="#PWR?"  Part="1" 
AR Path="/61B6C0DB" Ref="#PWR0102"  Part="1" 
F 0 "#PWR0102" H 5750 6650 50  0001 C CNN
F 1 "GND" H 5755 6727 50  0000 C CNN
F 2 "" H 5750 6900 50  0001 C CNN
F 3 "" H 5750 6900 50  0001 C CNN
	1    5750 6900
	1    0    0    -1  
$EndComp
Wire Wire Line
	6050 6800 6050 6900
$Comp
L power:GND #PWR?
U 1 1 61B6C6FF
P 6050 6900
AR Path="/6062503A/61B6C6FF" Ref="#PWR?"  Part="1" 
AR Path="/6065743C/61B6C6FF" Ref="#PWR?"  Part="1" 
AR Path="/61B6C6FF" Ref="#PWR0108"  Part="1" 
F 0 "#PWR0108" H 6050 6650 50  0001 C CNN
F 1 "GND" H 6055 6727 50  0000 C CNN
F 2 "" H 6050 6900 50  0001 C CNN
F 3 "" H 6050 6900 50  0001 C CNN
	1    6050 6900
	1    0    0    -1  
$EndComp
Wire Wire Line
	6350 6800 6350 6900
$Comp
L power:GND #PWR?
U 1 1 61B6CCDC
P 6350 6900
AR Path="/6062503A/61B6CCDC" Ref="#PWR?"  Part="1" 
AR Path="/6065743C/61B6CCDC" Ref="#PWR?"  Part="1" 
AR Path="/61B6CCDC" Ref="#PWR0109"  Part="1" 
F 0 "#PWR0109" H 6350 6650 50  0001 C CNN
F 1 "GND" H 6355 6727 50  0000 C CNN
F 2 "" H 6350 6900 50  0001 C CNN
F 3 "" H 6350 6900 50  0001 C CNN
	1    6350 6900
	1    0    0    -1  
$EndComp
Wire Wire Line
	6650 6800 6650 6900
$Comp
L power:GND #PWR?
U 1 1 61B6D37D
P 6650 6900
AR Path="/6062503A/61B6D37D" Ref="#PWR?"  Part="1" 
AR Path="/6065743C/61B6D37D" Ref="#PWR?"  Part="1" 
AR Path="/61B6D37D" Ref="#PWR0112"  Part="1" 
F 0 "#PWR0112" H 6650 6650 50  0001 C CNN
F 1 "GND" H 6655 6727 50  0000 C CNN
F 2 "" H 6650 6900 50  0001 C CNN
F 3 "" H 6650 6900 50  0001 C CNN
	1    6650 6900
	1    0    0    -1  
$EndComp
$Sheet
S 5150 3000 1350 2100
U 61B7A600
F0 "PWM Filter" 50
F1 "OpenFlowMeter_PWM_Filter.sch" 50
F2 "OUT1" O R 6500 3100 50 
F3 "OUT2" O R 6500 4650 50 
F4 "IN1" I L 5150 3100 50 
F5 "IN2" I L 5150 4650 50 
$EndSheet
Wire Wire Line
	7700 3100 6500 3100
Wire Wire Line
	7700 4650 6500 4650
Wire Wire Line
	7200 4750 7700 4750
Wire Wire Line
	7200 4850 7700 4850
Wire Wire Line
	7200 3300 7700 3300
Wire Wire Line
	7200 3200 7700 3200
$EndSCHEMATC
