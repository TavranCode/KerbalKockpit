/*
Adafruit Arduino - Lesson 3. RGB LED
*/
 
int cPowerBlue = 6;
int cPowerGreen = 5;
int cErrorRed = 8;
int cErrorBlue = 7;
 
//uncomment this line if using a Common Anode LED
//#define COMMON_ANODE
 
void setup()
{
  pinMode(cPowerBlue, OUTPUT);
  pinMode(cPowerGreen, OUTPUT);
  pinMode(cErrorRed, OUTPUT);  
  pinMode(cErrorBlue, OUTPUT);  
}
 
void loop()
{
  setPowerLED(HIGH, LOW);  // power green
  delay(1000);
  setPowerLED(LOW,HIGH); // power blue
  delay(1000);
  setPowerLED(LOW,LOW); // power off
  delay(1000);
  setErrorLED(HIGH, LOW);  // error red
  delay(1000);
  setErrorLED(LOW,HIGH); // error blue
  delay(1000);
  setErrorLED(LOW,LOW); //error off
  delay(1000);
}
 
void setPowerLED(int green, int blue)
{
  digitalWrite(cPowerGreen, green);
  digitalWrite(cPowerBlue, blue);  
}

void setErrorLED(int red, int blue)
{
  digitalWrite(cErrorRed, red);
  digitalWrite(cErrorBlue, blue);  
}
