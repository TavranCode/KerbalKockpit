/******************************************************************************
Multiple Analog Mux and hardcoded input test.
Based on: "SparkFun Multiplexer Analog Input Example
Jim Lindblom @ SparkFun Electronics
August 15, 2016
https://github.com/sparkfun/74HC4051_8-Channel_Mux_Breakout"


******************************************************************************/
/////////////////////
// Pin Definitions //
/////////////////////
const int selectPins[3] = {15, 16, 14}; // S0, S1, S2
const int zInputa = A0; // Connect common (Z) to A0 (analog input)
//const int DIMp = A1;
//const int bDIMp = A2;
void setup() 
{
  Serial.begin(9600); // Initialize the serial port
  // Set up the select pins as outputs:
  for (int i=0; i<3; i++)
  {
    pinMode(selectPins[i], OUTPUT);
    digitalWrite(selectPins[i], HIGH);
  }
  pinMode(zInputa, INPUT);
  //pinMode(DIMp, INPUT);
  //pinMode(bDIMp, INPUT);
}

// The selectMuxPin function sets the S0, S1, and S2 pins
// accordingly, given a pin from 0-7.
void selectAMuxPin(byte pin)
{
  for (int i=0; i<3; i++)
  {
    if (pin & (1<<i))
      digitalWrite(selectPins[i], HIGH);
    else
      digitalWrite(selectPins[i], LOW);
  }
}

void loop() 
{
  Serial.print(0);
  Serial.print(" ");
    
  // Loop through the hard wired dimmers
  //Serial.print(String(analogRead(DIMp)/4)+" ");
  //Serial.print(String(analogRead(bDIMp)/4)+" ");
  //Serial.print(String(analogRead(zInputa))+" "); //read pin 8, the default (111)
  
  // Loop through pins.
  for (byte pin=6; pin<=6; pin++)
  {
    selectAMuxPin(pin); // Select one at a time
    //delayMicroseconds(500);
    int inputValuea = analogRead(zInputa); // and read Z
    //delayMicroseconds(150);
    //inputValuea = analogRead(zInputa)/4; // and read Z
    Serial.print(String(inputValuea) + " ");
  }
  Serial.println(1023);
}
