#include <Sparkfun_DRV2605L.h>
#include <Wire.h> //I2C library 

SFE_HMD_DRV2605L HMD; //Create haptic motor driver object 

void setup() 
{
  HMD.begin();    
  Serial.begin(9600);
  HMD.Mode(0); // Internal trigger input mode -- Must use the GO() function to trigger playback.
  HMD.MotorSelect(0x36); // ERM motor, 4x Braking, Medium loop gain, 1.365x back EMF gain
  HMD.Library(2); //1-5 & 7 for ERM motors, 6 for LRA motors 
}
void loop() 
{
  int seq = 0; //There are 8 sequence registers that can queue up to 8 waveforms
  HMD.Waveform(seq, 47);
  HMD.Waveform(1, 47);
  HMD.Waveform(2, 47);
  HMD.Waveform(3, 47);
  HMD.Waveform(4, 47);
  HMD.Waveform(5, 47);
  HMD.Waveform(6, 47);
  HMD.Waveform(7, 47);
  HMD.go();
 }
