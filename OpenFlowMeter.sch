EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 7
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
S 1000 1000 2150 500 
U 606200AB
F0 "Controller" 50
F1 "OpenFlowMeter_Controller.sch" 50
$EndSheet
$Sheet
S 5100 3000 1650 550 
U 60624FF4
F0 "DAC 1" 50
F1 "OpenFlowMeter_DAC.sch" 50
F2 "Uout" O R 6750 3100 50 
F3 "SCL" I L 5100 3100 50 
F4 "SDA" B L 5100 3200 50 
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
Wire Wire Line
	7700 3100 6750 3100
$Sheet
S 5100 3800 1650 500 
U 6062EBC0
F0 "ADC" 50
F1 "OpenFlowMeter_ADC.sch" 50
F2 "IN0" I R 6750 3900 50 
F3 "IN1" I R 6750 4000 50 
F4 "IN2" I R 6750 4100 50 
F5 "IN3" I R 6750 4200 50 
F6 "SCL" I L 5100 4000 50 
F7 "SDA" B L 5100 4100 50 
$EndSheet
Wire Wire Line
	6750 3900 7400 3900
Wire Wire Line
	7400 3900 7400 3200
Wire Wire Line
	7400 3200 7700 3200
Wire Wire Line
	6750 4000 7500 4000
Wire Wire Line
	7500 4000 7500 3300
Wire Wire Line
	7500 3300 7700 3300
$Comp
L Device:R R14
U 1 1 6064B5B5
P 10250 1200
F 0 "R14" H 10320 1246 50  0000 L CNN
F 1 "10k" H 10320 1155 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad0.98x0.95mm_HandSolder" V 10180 1200 50  0001 C CNN
F 3 "~" H 10250 1200 50  0001 C CNN
	1    10250 1200
	1    0    0    -1  
$EndComp
$Comp
L Device:R R13
U 1 1 6064C030
P 9950 1200
F 0 "R13" H 10020 1246 50  0000 L CNN
F 1 "10k" H 10020 1155 50  0000 L CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad0.98x0.95mm_HandSolder" V 9880 1200 50  0001 C CNN
F 3 "~" H 9950 1200 50  0001 C CNN
	1    9950 1200
	1    0    0    -1  
$EndComp
Text Label 5000 4000 2    50   ~ 0
SCL
Text Label 5000 4100 2    50   ~ 0
SDA
Text Label 5000 3100 2    50   ~ 0
SCL
Text Label 5000 3200 2    50   ~ 0
SDA
Wire Wire Line
	4800 3100 5100 3100
Wire Wire Line
	4800 3200 5100 3200
$Sheet
S 5100 4550 1650 550 
U 606570C9
F0 "DAC 2" 50
F1 "OpenFlowMeter_DAC.sch" 50
F2 "Uout" O R 6750 4650 50 
F3 "SCL" I L 5100 4650 50 
F4 "SDA" B L 5100 4750 50 
$EndSheet
Wire Wire Line
	7700 4650 6750 4650
Text Label 5000 4650 2    50   ~ 0
SCL
Text Label 5000 4750 2    50   ~ 0
SDA
Wire Wire Line
	4800 4650 5100 4650
Wire Wire Line
	4800 4750 5100 4750
$Sheet
S 7700 4550 1800 550 
U 6065743C
F0 "Current Source 2" 50
F1 "OpenFlowMeter_CurrentSource.sch" 50
F2 "ISET" I L 7700 4650 50 
F3 "IMEAS" O L 7700 4750 50 
F4 "UMEAS" O L 7700 4850 50 
$EndSheet
Text Label 10550 1400 2    50   ~ 0
SCL
Text Label 10550 1500 2    50   ~ 0
SDA
Wire Wire Line
	10650 1400 10250 1400
Wire Wire Line
	10650 1500 9950 1500
Wire Wire Line
	10250 1400 10250 1350
Connection ~ 10250 1400
Wire Wire Line
	10250 1400 9500 1400
Wire Wire Line
	9950 1500 9950 1350
Connection ~ 9950 1500
Wire Wire Line
	9950 1500 9500 1500
Wire Wire Line
	4800 4100 5100 4100
Wire Wire Line
	4800 4000 5100 4000
Wire Wire Line
	7700 4750 7500 4750
Wire Wire Line
	7500 4750 7500 4100
Wire Wire Line
	7500 4100 6750 4100
Wire Wire Line
	7700 4850 7400 4850
Wire Wire Line
	7400 4850 7400 4200
Wire Wire Line
	7400 4200 6750 4200
Text Notes 5100 2750 0    118  ~ 24
Powered with 3V3
Text Notes 7700 2750 0    118  ~ 24
Powered with 24V
Text Notes 7050 6800 0    118  ~ 0
Two channel flow meter.
$EndSCHEMATC
