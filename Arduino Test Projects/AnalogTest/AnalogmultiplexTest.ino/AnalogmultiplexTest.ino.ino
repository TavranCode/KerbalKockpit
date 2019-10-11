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
const int selectPins[3] = {8, 12, 13}; // S0, S1, S2
const int zInputa = A0; // Connect common (Z) to A0 (analog input)
const int zInputb = A1; // Connect common (Z) to A0 (analog input)
const int DIMp = A2;
const int bDIMp = A3;
void setup() 
{
  Serial.begin(9600); // Initialize the serial port
  // Set up the select pins as outputs:
  for (int i=0; i<3; i++)
  {
    pinMode(selectPins[i], OUTPUT);
    digitalWrite(selectPins[i], HIGH);
  }
  pinMode(zInputa, INPUT); // Set up Z as an input
  pinMode(zInputb, INPUT);
  pinMode(DIMp, INPUT);
  pinMode(bDIMp, INPUT);

  // Print the header:
//  Serial.println("Y0\tY1\tY2\tY3\tY4\tY5\tY6\tY7");
//  Serial.println("---\t---\t---\t---\t---\t---\t---\t---");
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
  // Loop through the hard wired dimmers
  //Serial.print(String(analogRead(DIMp))+" ");
  //Serial.print(String(analogRead(bDIMp))+" ");
  // Loop through all eight pins.
  for (byte pin=0; pin<=7; pin++)
  {
    selectAMuxPin(pin); // Select one at a time
    int inputValuea = analogRead(zInputa); // and read Z1
    int inputValueb = analogRead(zInputb); // and read Z2
    //Serial.print(String(inputValuea) + " " + String(inputValueb) + " ");
    Serial.print(String(inputValueb) + " ");
  }
  Serial.println();
}
