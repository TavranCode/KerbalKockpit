// This script tests the v3 button matrix
#include <Wire.h>
  const byte mcp_address=0x20;      // I2C Address of MCP23017 Chip
  const byte IODIRA=0x00;
  const byte GPIOA=0x12;            // Register Address of Port A
  const byte GPIOB=0x13;            // Register Address of Port B
  const byte qrows[] = {0b11111110,0b11111101,0b11111011};
  
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
    Serial.print(var  & test ? '1' : '0');
  }
}

void setup() {
  Serial.begin(9600); // Initialize the serial port
  Wire.begin();
  mux_Tx(mcp_address, 0x00, 0x00);  /* MUX 0x23, IODIRA, Set all to output (0) */
}

void loop() {
  for (int row = 0; row < 8; row++) { 
    byte buff=0;
    mux_Tx(mcp_address,GPIOA,qrows[row]);
    mux_Rx(mcp_address, 0x13,1,&buff);
    printBin(buff);
    Serial.print(" ");
  }
  Serial.print("\n");
  delay(100);

}
