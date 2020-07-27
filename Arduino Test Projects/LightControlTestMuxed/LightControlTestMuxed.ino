#include <Wire.h>

void mux_Tx(int adr, int reg, byte data) {
  /* This function will send data to a MCP23017 chip */
  Wire.beginTransmission(adr);     /* address the chip */
  Wire.write(reg);                 /* point to the register of choice */
  Wire.write(data);                /* send the data */
  Wire.endTransmission();          /* end the transmission */
}

const int p_Dim = 11;
const int analogInPin = A1;
const int p_powerled = 5;
const int p_errled = A7;
int sensorValue=0;
int outputValue=200;


void setup() {
  Wire.begin();
  mux_Tx(0x21, 0x00, 0x00);  /* MUX 0x23, IODIRA, Set all to output (0) */
  mux_Tx(0x21, 0x01, 0x00);  /* MUX 0x23, IODIRB, Set all to output (0) */
  Serial.begin(9600);
  mux_Tx(0x21,0x12, 0xFF); 
  mux_Tx(0x21,0x13, 0xFF); 
  
  pinMode(p_powerled,OUTPUT);
  pinMode(p_errled,OUTPUT);
  pinMode(analogInPin,INPUT);
  pinMode(p_Dim,OUTPUT);
}

void loop() {
  // read the analog in value:
  sensorValue = analogRead(analogInPin);
  // map it to the range of the analog out:
  outputValue = map(sensorValue, 0, 1023, 250, 0); // map(sensorValue, 0, 1023, 250, 0);
  // change the analog out value and print it:
  analogWrite(p_Dim, outputValue); 
  analogWrite(p_powerled,outputValue);
  analogWrite(p_errled,outputValue);
  mux_Tx(0x21,0x12,0xFF); 
  mux_Tx(0x21,0x13,0xFF);
  delay(300);
  analogWrite(p_powerled,0);
  analogWrite(p_errled,0);
  mux_Tx(0x21,0x12,0x00); 
  mux_Tx(0x21,0x13,0x00);
  delay(300);
  }
