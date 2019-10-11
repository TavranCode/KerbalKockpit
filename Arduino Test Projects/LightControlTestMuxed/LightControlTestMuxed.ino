#include <Wire.h>


void mux_Tx(int adr, int reg, byte data) {
  /* This function will send data to a MCP23017 chip */
  Wire.beginTransmission(adr);     /* address the chip */
  Wire.write(reg);                 /* point to the register of choice */
  Wire.write(data);                /* send the data */
  Wire.endTransmission();          /* end the transmission */
}

const int analogInPin = A2;  // Analog input pin that the potentiometer is attached to

int sensorValue = 0;        // value read from the pot
int outputValue = 0;        // value output to the PWM (analog out)
int outputValuei = 0;       // value output to the PWM inverted

const int dimmerpin = 9;

// The number we're going to display.
byte count;
byte fcount;

const int on = 255;
const int off = 0;

void setup() {
{
  Wire.begin();
  mux_Tx(0x27, 0x00, 0x00);  /* MUX 0x23, IODIRA, Set all to output (0) */
  count = 0;
  fcount = 0;
}
    Serial.begin(9600);
}

void loop() {
  // read the analog in value:
  sensorValue = analogRead(analogInPin);
  // map it to the range of the analog out:
  outputValue = map(sensorValue, 0, 1023, 250, 0);
  outputValuei = map(sensorValue, 0, 1023, 0, 250);
  // change the analog out value:
  // analogWrite(analogOutPin, outputValue);
  analogWrite(dimmerpin,outputValuei);
  if(fcount % 25 == 0) {
    count++;
  }
  
  //mux_Tx(0x27,0x00, count % 256); 
  mux_Tx(0x27,0x00, 0xFF); 
  mux_Tx(0x27,0x01, 0xFF); 

  fcount++;
  
  Serial.print("fcount = ");
  Serial.print(fcount);
  Serial.print("\t count = ");
  Serial.print(count);
  Serial.print("\t analog = ");
  Serial.print(outputValue);
  Serial.print("\t analog2 = ");
  Serial.println(outputValuei);
  delay(20);
}
