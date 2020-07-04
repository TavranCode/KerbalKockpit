#include <Wire.h>

void mux_Tx(int adr, int reg, byte data) {
  /* This function will send data to a MCP23017 chip */
  Wire.beginTransmission(adr);     /* address the chip */
  Wire.write(reg);                 /* point to the register of choice */
  Wire.write(data);                /* send the data */
  Wire.endTransmission();          /* end the transmission */
}

void mux_Rx(int adr, int reg, int numbytes, byte *data) {
  /* This function will request n bytes of data from a MCP23017 chip */
  Wire.beginTransmission(adr);     /* address the chip */
  Wire.write(reg);                 /* point to the register of choice */
  Wire.endTransmission();          /* end the transmission */
  Wire.requestFrom(adr, numbytes); /* request the data */
  *data = Wire.read();
}

void printBin(int var) {
  for (unsigned int test = 0x80; test; test >>= 1) {
    Serial.println(var  & test ? '1' : '0');
  }
}

//Now Setup output, including dimmers
  const int analogInPin = A3;
  const int dimmerpin = 9;
  int sensorValue = 0;        // value read from the pot
  int outputValue = 0;        // value output to the PWM (analog out)
  int lightcode = 0;
  byte lights=0xFF;
  int sysPins[] = { 3, 5, 6 };
  int pinCount = 3;

void setup() {
  //system lights on
  
  for (int thisPin = 0; thisPin < pinCount; thisPin++) {
    pinMode(sysPins[thisPin],OUTPUT);
  }
  
  //First set up the input muxing
  Serial.begin(9600); // Initialize the serial port
  Serial.print("I'm awake!\n");
  /* wake up the I2C_bus */
  int n_mux_chips_detected = 0;           /* number of MUX chips detected in the IBIT */
  const int c_num_mux_chips = 2;
  const int c_first_mux_address = 0x20;     /* the first I2C address in the MUX range [-]*/
  const int c_last_mux_address = 0x21;      /* the last I2C address in the MUX range [-]*/
  
  Wire.begin();
  Serial.print("Started Wire\n");
  /* check we have all the MCP23017 chips */
//  for (byte a = c_first_mux_address; a <= c_last_mux_address; a++)   /* chip addresses start at 0x20, max of 8 chips */
//  {
//    Serial.print("Testing ");
//    Serial.print(a);
//    Wire.beginTransmission (a);
//    int testval = Wire.endTransmission ();
//    Serial.print(" returned ");
//    Serial.print(testval);
//    Serial.print("\n");
//    if (testval == 0) {
//      n_mux_chips_detected++;
//    }
//  }
//  
//  Serial.print("Done testing, detected: ");
//  Serial.print(n_mux_chips_detected);
//  Serial.print("\n");
//  if (n_mux_chips_detected != c_num_mux_chips) {
//    Serial.print("mux miss");
//  }

  Wire.begin();
  mux_Tx(0x27, 0x00, 0x00);  /* MUX 0x23, IODIRA, Set all to output (0) */
  
}

void loop() {
//handle dimmer

  sensorValue = analogRead(analogInPin);
  outputValue = map(sensorValue, 0, 1023, 250, 0);
  analogWrite(dimmerpin, outputValue);

//read Input Buttons
  byte buffb=0;
  mux_Rx(0x20, // i2c 0
         0x13, // GPIOB
         1, // Start at register 1
         &buffb); //write to buff
  byte buffa=0;
  mux_Rx(0x20, // i2c 0
         0x12, // GPIOA
         1, // Start at register 1
         &buffa); //write to buff

  lights = lights ^ buffb;
  Serial.print("Dimmer is: ");
  Serial.print(outputValue);
  
  mux_Tx(0x27,0x12, lights); 
  mux_Tx(0x27,0x13, lights);  
  for (int thisPin = 0; thisPin < pinCount; thisPin++) {
    analogWrite(sysPins[thisPin], outputValue);
  }
  delay(100);

}
