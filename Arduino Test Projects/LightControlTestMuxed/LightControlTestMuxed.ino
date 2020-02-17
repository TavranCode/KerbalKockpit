#include <Wire.h>


void mux_Tx(int adr, int reg, byte data) {
  /* This function will send data to a MCP23017 chip */
  Wire.beginTransmission(adr);     /* address the chip */
  Wire.write(reg);                 /* point to the register of choice */
  Wire.write(data);                /* send the data */
  Wire.endTransmission();          /* end the transmission */
}

const int dimmerpin = 9;


void setup() {
{
  Wire.begin();
  mux_Tx(0x27, 0x00, 0x00);  /* MUX 0x23, IODIRA, Set all to output (0) */
  mux_Tx(0x27, 0x01, 0x00);  /* MUX 0x23, IODIRB, Set all to output (0) */
}
    Serial.begin(9600);
      mux_Tx(0x27,0x12, 0xFF); 
      mux_Tx(0x27,0x13, 0xFF); 

}

void loop() {
  // read the analog in value:
  // sensorValue = analogRead(analogInPin);
  // map it to the range of the analog out:
  //outputValue = 200; // map(sensorValue, 0, 1023, 250, 0);
  //outputValuei = 200; // map(sensorValue, 0, 1023, 0, 250);
  // change the analog out value:
  // analogWrite(analogOutPin, outputValue);
    for (int fadeValue = 0 ; fadeValue <= 255; fadeValue += 5) {
    // sets the value (range from 0 to 255):
    analogWrite(dimmerpin, fadeValue);
    // wait for 30 milliseconds to see the dimming effect
    delay(30);
  }

  // fade out from max to min in increments of 5 points:
  for (int fadeValue = 255 ; fadeValue >= 0; fadeValue -= 5) {
    // sets the value (range from 0 to 255):
    analogWrite(dimmerpin, fadeValue);
    // wait for 30 milliseconds to see the dimming effect
    delay(30);
  }
  
  //mux_Tx(0x27,0x00, count % 256); 

}
