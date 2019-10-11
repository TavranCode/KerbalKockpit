EESchema Schematic File Version 4
LIBS:testing-cache
EELAYER 26 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 1 1
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
L Interface_Expansion:MCP23017_SP U1
U 1 1 5C2AC97D
P 3150 3350
F 0 "U1" H 3150 4628 50  0000 C CNN
F 1 "MCP23017_SP" H 3150 4537 50  0000 C CNN
F 2 "Package_DIP:DIP-28_W7.62mm_Socket" H 3350 2350 50  0001 L CNN
F 3 "http://ww1.microchip.com/downloads/en/DeviceDoc/20001952C.pdf" H 3350 2250 50  0001 L CNN
	1    3150 3350
	-1   0    0    -1  
$EndComp
$Comp
L Transistor_Array:ULN2804A U2
U 1 1 5C2AC9FC
P 5050 2750
F 0 "U2" H 5050 3317 50  0000 C CNN
F 1 "ULN2804A" H 5050 3226 50  0000 C CNN
F 2 "Package_DIP:DIP-18_W7.62mm_Socket" H 5100 2100 50  0001 L CNN
F 3 "http://www.promelec.ru/pdf/1536.pdf" H 5150 2550 50  0001 C CNN
	1    5050 2750
	1    0    0    -1  
$EndComp
Entry Wire Line
	4550 3150 4650 3250
Entry Wire Line
	4550 3050 4650 3150
Entry Wire Line
	4550 2950 4650 3050
Entry Wire Line
	4550 2850 4650 2950
Entry Wire Line
	4550 2750 4650 2850
Entry Wire Line
	4550 2650 4650 2750
Entry Wire Line
	4550 2550 4650 2650
Entry Wire Line
	4550 2450 4650 2550
Entry Wire Line
	2350 2450 2450 2550
Entry Wire Line
	2350 2550 2450 2650
Entry Wire Line
	2350 2650 2450 2750
Entry Wire Line
	2350 2750 2450 2850
Entry Wire Line
	2350 2850 2450 2950
Entry Wire Line
	2350 2950 2450 3050
Entry Wire Line
	2350 3050 2450 3150
Entry Wire Line
	2350 3150 2450 3250
Wire Bus Line
	2350 2150 4550 2150
Wire Bus Line
	2350 2150 2350 3150
Wire Bus Line
	4550 2150 4550 3150
$EndSCHEMATC
