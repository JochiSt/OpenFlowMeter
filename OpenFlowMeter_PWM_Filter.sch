EESchema Schematic File Version 4
EELAYER 30 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 5 5
Title ""
Date ""
Rev ""
Comp ""
Comment1 ""
Comment2 ""
Comment3 ""
Comment4 ""
$EndDescr
$Comp
L Amplifier_Operational:LT1492 U?
U 1 1 61B7F473
P 5800 3600
AR Path="/6062503A/61B7F473" Ref="U?"  Part="1" 
AR Path="/6065743C/61B7F473" Ref="U?"  Part="1" 
AR Path="/61B7F473" Ref="U?"  Part="1" 
AR Path="/61B7A600/61B7F473" Ref="U3"  Part="1" 
F 0 "U3" H 5800 3967 50  0000 C CNN
F 1 "LT1492" H 5800 3876 50  0000 C CNN
F 2 "Package_SO:OnSemi_Micro8" H 5800 3600 50  0001 C CNN
F 3 "https://www.analog.com/media/en/technical-documentation/data-sheets/14923f.pdf" H 5800 3600 50  0001 C CNN
	1    5800 3600
	1    0    0    1   
$EndComp
$Comp
L Amplifier_Operational:LT1492 U?
U 3 1 61B7F479
P 5950 2350
AR Path="/6062503A/61B7F479" Ref="U?"  Part="3" 
AR Path="/6065743C/61B7F479" Ref="U?"  Part="3" 
AR Path="/61B7F479" Ref="U?"  Part="3" 
AR Path="/61B7A600/61B7F479" Ref="U3"  Part="3" 
F 0 "U3" H 5908 2396 50  0000 L CNN
F 1 "LT1492" H 5908 2305 50  0000 L CNN
F 2 "Package_SO:OnSemi_Micro8" H 5950 2350 50  0001 C CNN
F 3 "https://www.analog.com/media/en/technical-documentation/data-sheets/14923f.pdf" H 5950 2350 50  0001 C CNN
	3    5950 2350
	1    0    0    -1  
$EndComp
Wire Wire Line
	5850 2650 5850 2750
$Comp
L power:GND #PWR?
U 1 1 61B7F486
P 5850 2750
AR Path="/6062503A/61B7F486" Ref="#PWR?"  Part="1" 
AR Path="/6065743C/61B7F486" Ref="#PWR?"  Part="1" 
AR Path="/61B7F486" Ref="#PWR?"  Part="1" 
AR Path="/61B7A600/61B7F486" Ref="#PWR017"  Part="1" 
F 0 "#PWR017" H 5850 2500 50  0001 C CNN
F 1 "GND" H 5855 2577 50  0000 C CNN
F 2 "" H 5850 2750 50  0001 C CNN
F 3 "" H 5850 2750 50  0001 C CNN
	1    5850 2750
	1    0    0    -1  
$EndComp
Wire Wire Line
	5850 2050 5850 1950
$Comp
L Device:C C?
U 1 1 61B7F48D
P 6400 2350
AR Path="/6062503A/61B7F48D" Ref="C?"  Part="1" 
AR Path="/6065743C/61B7F48D" Ref="C?"  Part="1" 
AR Path="/61B7F48D" Ref="C?"  Part="1" 
AR Path="/61B7A600/61B7F48D" Ref="C9"  Part="1" 
F 0 "C9" H 6515 2396 50  0000 L CNN
F 1 "C" H 6515 2305 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric_Pad1.05x0.95mm_HandSolder" H 6438 2200 50  0001 C CNN
F 3 "~" H 6400 2350 50  0001 C CNN
	1    6400 2350
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 61B7F493
P 6400 2750
AR Path="/6062503A/61B7F493" Ref="#PWR?"  Part="1" 
AR Path="/6065743C/61B7F493" Ref="#PWR?"  Part="1" 
AR Path="/61B7F493" Ref="#PWR?"  Part="1" 
AR Path="/61B7A600/61B7F493" Ref="#PWR018"  Part="1" 
F 0 "#PWR018" H 6400 2500 50  0001 C CNN
F 1 "GND" H 6405 2577 50  0000 C CNN
F 2 "" H 6400 2750 50  0001 C CNN
F 3 "" H 6400 2750 50  0001 C CNN
	1    6400 2750
	1    0    0    -1  
$EndComp
Wire Wire Line
	6400 1950 6400 2200
Wire Wire Line
	6400 2500 6400 2750
$Comp
L Amplifier_Operational:LT1492 U?
U 2 1 61B875C0
P 5800 4900
AR Path="/6062503A/61B875C0" Ref="U?"  Part="1" 
AR Path="/6065743C/61B875C0" Ref="U?"  Part="1" 
AR Path="/61B875C0" Ref="U?"  Part="1" 
AR Path="/61B7A600/61B875C0" Ref="U3"  Part="2" 
F 0 "U3" H 5800 5267 50  0000 C CNN
F 1 "LT1492" H 5800 5176 50  0000 C CNN
F 2 "Package_SO:OnSemi_Micro8" H 5800 4900 50  0001 C CNN
F 3 "https://www.analog.com/media/en/technical-documentation/data-sheets/14923f.pdf" H 5800 4900 50  0001 C CNN
	2    5800 4900
	1    0    0    1   
$EndComp
Wire Wire Line
	5500 3500 5400 3500
Wire Wire Line
	5400 3500 5400 3300
Wire Wire Line
	5400 3300 6250 3300
Wire Wire Line
	6250 3300 6250 3600
Wire Wire Line
	6250 3600 6100 3600
Wire Wire Line
	6100 4900 6250 4900
Wire Wire Line
	6250 4900 6250 4600
Wire Wire Line
	6250 4600 5400 4600
Wire Wire Line
	5400 4600 5400 4800
Wire Wire Line
	5400 4800 5500 4800
Wire Wire Line
	6250 3600 7500 3600
Connection ~ 6250 3600
Wire Wire Line
	6250 4900 7500 4900
Connection ~ 6250 4900
Text HLabel 7500 3600 2    50   Output ~ 0
OUT1
Text HLabel 7500 4900 2    50   Output ~ 0
OUT2
Text HLabel 3450 3700 0    50   Input ~ 0
IN1
Text HLabel 3450 5000 0    50   Input ~ 0
IN2
$Comp
L Device:R R?
U 1 1 61B8D92C
P 4100 3700
AR Path="/6062503A/61B8D92C" Ref="R?"  Part="1" 
AR Path="/6065743C/61B8D92C" Ref="R?"  Part="1" 
AR Path="/61B7A600/61B8D92C" Ref="R8"  Part="1" 
F 0 "R8" V 3893 3700 50  0000 C CNN
F 1 "1k" V 3984 3700 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad0.98x0.95mm_HandSolder" V 4030 3700 50  0001 C CNN
F 3 "~" H 4100 3700 50  0001 C CNN
	1    4100 3700
	0    1    1    0   
$EndComp
Wire Wire Line
	3950 3700 3450 3700
$Comp
L Device:R R?
U 1 1 61B8DDFD
P 4900 3700
AR Path="/6062503A/61B8DDFD" Ref="R?"  Part="1" 
AR Path="/6065743C/61B8DDFD" Ref="R?"  Part="1" 
AR Path="/61B7A600/61B8DDFD" Ref="R29"  Part="1" 
F 0 "R29" V 4693 3700 50  0000 C CNN
F 1 "1k" V 4784 3700 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad0.98x0.95mm_HandSolder" V 4830 3700 50  0001 C CNN
F 3 "~" H 4900 3700 50  0001 C CNN
	1    4900 3700
	0    1    1    0   
$EndComp
Wire Wire Line
	4750 3700 4500 3700
$Comp
L Device:C C?
U 1 1 61B8EB97
P 4500 3900
AR Path="/6062503A/61B8EB97" Ref="C?"  Part="1" 
AR Path="/6065743C/61B8EB97" Ref="C?"  Part="1" 
AR Path="/61B8EB97" Ref="C?"  Part="1" 
AR Path="/61B7A600/61B8EB97" Ref="C5"  Part="1" 
F 0 "C5" H 4615 3946 50  0000 L CNN
F 1 "C" H 4615 3855 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric_Pad1.05x0.95mm_HandSolder" H 4538 3750 50  0001 C CNN
F 3 "~" H 4500 3900 50  0001 C CNN
	1    4500 3900
	1    0    0    -1  
$EndComp
$Comp
L Device:C C?
U 1 1 61B8F4DE
P 5150 3900
AR Path="/6062503A/61B8F4DE" Ref="C?"  Part="1" 
AR Path="/6065743C/61B8F4DE" Ref="C?"  Part="1" 
AR Path="/61B8F4DE" Ref="C?"  Part="1" 
AR Path="/61B7A600/61B8F4DE" Ref="C7"  Part="1" 
F 0 "C7" H 5265 3946 50  0000 L CNN
F 1 "C" H 5265 3855 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric_Pad1.05x0.95mm_HandSolder" H 5188 3750 50  0001 C CNN
F 3 "~" H 5150 3900 50  0001 C CNN
	1    5150 3900
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 61B8FA19
P 5150 4100
AR Path="/6062503A/61B8FA19" Ref="#PWR?"  Part="1" 
AR Path="/6065743C/61B8FA19" Ref="#PWR?"  Part="1" 
AR Path="/61B8FA19" Ref="#PWR?"  Part="1" 
AR Path="/61B7A600/61B8FA19" Ref="#PWR09"  Part="1" 
F 0 "#PWR09" H 5150 3850 50  0001 C CNN
F 1 "GND" H 5155 3927 50  0000 C CNN
F 2 "" H 5150 4100 50  0001 C CNN
F 3 "" H 5150 4100 50  0001 C CNN
	1    5150 4100
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 61B8FF12
P 4500 4100
AR Path="/6062503A/61B8FF12" Ref="#PWR?"  Part="1" 
AR Path="/6065743C/61B8FF12" Ref="#PWR?"  Part="1" 
AR Path="/61B8FF12" Ref="#PWR?"  Part="1" 
AR Path="/61B7A600/61B8FF12" Ref="#PWR01"  Part="1" 
F 0 "#PWR01" H 4500 3850 50  0001 C CNN
F 1 "GND" H 4505 3927 50  0000 C CNN
F 2 "" H 4500 4100 50  0001 C CNN
F 3 "" H 4500 4100 50  0001 C CNN
	1    4500 4100
	1    0    0    -1  
$EndComp
Wire Wire Line
	5150 4100 5150 4050
Wire Wire Line
	4500 4100 4500 4050
Wire Wire Line
	4500 3750 4500 3700
Connection ~ 4500 3700
Wire Wire Line
	4500 3700 4250 3700
Wire Wire Line
	5050 3700 5150 3700
Wire Wire Line
	5150 3700 5150 3750
Wire Wire Line
	5150 3700 5500 3700
Connection ~ 5150 3700
$Comp
L Device:R R?
U 1 1 61B97FD2
P 4100 5000
AR Path="/6062503A/61B97FD2" Ref="R?"  Part="1" 
AR Path="/6065743C/61B97FD2" Ref="R?"  Part="1" 
AR Path="/61B7A600/61B97FD2" Ref="R22"  Part="1" 
F 0 "R22" V 3893 5000 50  0000 C CNN
F 1 "1k" V 3984 5000 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad0.98x0.95mm_HandSolder" V 4030 5000 50  0001 C CNN
F 3 "~" H 4100 5000 50  0001 C CNN
	1    4100 5000
	0    1    1    0   
$EndComp
Wire Wire Line
	3950 5000 3450 5000
$Comp
L Device:R R?
U 1 1 61B97FD9
P 4900 5000
AR Path="/6062503A/61B97FD9" Ref="R?"  Part="1" 
AR Path="/6065743C/61B97FD9" Ref="R?"  Part="1" 
AR Path="/61B7A600/61B97FD9" Ref="R30"  Part="1" 
F 0 "R30" V 4693 5000 50  0000 C CNN
F 1 "1k" V 4784 5000 50  0000 C CNN
F 2 "Resistor_SMD:R_0603_1608Metric_Pad0.98x0.95mm_HandSolder" V 4830 5000 50  0001 C CNN
F 3 "~" H 4900 5000 50  0001 C CNN
	1    4900 5000
	0    1    1    0   
$EndComp
Wire Wire Line
	4750 5000 4500 5000
$Comp
L Device:C C?
U 1 1 61B97FE0
P 4500 5200
AR Path="/6062503A/61B97FE0" Ref="C?"  Part="1" 
AR Path="/6065743C/61B97FE0" Ref="C?"  Part="1" 
AR Path="/61B97FE0" Ref="C?"  Part="1" 
AR Path="/61B7A600/61B97FE0" Ref="C6"  Part="1" 
F 0 "C6" H 4615 5246 50  0000 L CNN
F 1 "C" H 4615 5155 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric_Pad1.05x0.95mm_HandSolder" H 4538 5050 50  0001 C CNN
F 3 "~" H 4500 5200 50  0001 C CNN
	1    4500 5200
	1    0    0    -1  
$EndComp
$Comp
L Device:C C?
U 1 1 61B97FE6
P 5150 5200
AR Path="/6062503A/61B97FE6" Ref="C?"  Part="1" 
AR Path="/6065743C/61B97FE6" Ref="C?"  Part="1" 
AR Path="/61B97FE6" Ref="C?"  Part="1" 
AR Path="/61B7A600/61B97FE6" Ref="C8"  Part="1" 
F 0 "C8" H 5265 5246 50  0000 L CNN
F 1 "C" H 5265 5155 50  0000 L CNN
F 2 "Capacitor_SMD:C_0603_1608Metric_Pad1.05x0.95mm_HandSolder" H 5188 5050 50  0001 C CNN
F 3 "~" H 5150 5200 50  0001 C CNN
	1    5150 5200
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 61B97FEC
P 5150 5400
AR Path="/6062503A/61B97FEC" Ref="#PWR?"  Part="1" 
AR Path="/6065743C/61B97FEC" Ref="#PWR?"  Part="1" 
AR Path="/61B97FEC" Ref="#PWR?"  Part="1" 
AR Path="/61B7A600/61B97FEC" Ref="#PWR010"  Part="1" 
F 0 "#PWR010" H 5150 5150 50  0001 C CNN
F 1 "GND" H 5155 5227 50  0000 C CNN
F 2 "" H 5150 5400 50  0001 C CNN
F 3 "" H 5150 5400 50  0001 C CNN
	1    5150 5400
	1    0    0    -1  
$EndComp
$Comp
L power:GND #PWR?
U 1 1 61B97FF2
P 4500 5400
AR Path="/6062503A/61B97FF2" Ref="#PWR?"  Part="1" 
AR Path="/6065743C/61B97FF2" Ref="#PWR?"  Part="1" 
AR Path="/61B97FF2" Ref="#PWR?"  Part="1" 
AR Path="/61B7A600/61B97FF2" Ref="#PWR08"  Part="1" 
F 0 "#PWR08" H 4500 5150 50  0001 C CNN
F 1 "GND" H 4505 5227 50  0000 C CNN
F 2 "" H 4500 5400 50  0001 C CNN
F 3 "" H 4500 5400 50  0001 C CNN
	1    4500 5400
	1    0    0    -1  
$EndComp
Wire Wire Line
	5150 5400 5150 5350
Wire Wire Line
	4500 5400 4500 5350
Wire Wire Line
	4500 5050 4500 5000
Connection ~ 4500 5000
Wire Wire Line
	4500 5000 4250 5000
Wire Wire Line
	5050 5000 5150 5000
Wire Wire Line
	5150 5000 5150 5050
Wire Wire Line
	5150 5000 5500 5000
Connection ~ 5150 5000
$Comp
L power:+3.3V #PWR019
U 1 1 61B99DCF
P 5850 1950
F 0 "#PWR019" H 5850 1800 50  0001 C CNN
F 1 "+3.3V" H 5865 2123 50  0000 C CNN
F 2 "" H 5850 1950 50  0001 C CNN
F 3 "" H 5850 1950 50  0001 C CNN
	1    5850 1950
	1    0    0    -1  
$EndComp
$Comp
L power:+3.3V #PWR020
U 1 1 61B9A73A
P 6400 1950
F 0 "#PWR020" H 6400 1800 50  0001 C CNN
F 1 "+3.3V" H 6415 2123 50  0000 C CNN
F 2 "" H 6400 1950 50  0001 C CNN
F 3 "" H 6400 1950 50  0001 C CNN
	1    6400 1950
	1    0    0    -1  
$EndComp
Text Notes 7000 6950 0    98   ~ 20
Buffered two stage RC filter for filtering & averaging\nSmoothening
$EndSCHEMATC
