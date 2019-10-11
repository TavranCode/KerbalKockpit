
const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to

int sensorValue = 0;        // value read from the pot
int outputValue;
int timeelapsed;
int prevtime=0;

void setup() {
  timeelapsed = 0;
  Serial.begin(115200);
}

void loop() {
  // read the analog in value:
  sensorValue = analogRead(analogInPin);
  // map it to the range of the analog out:
  outputValue = map(sensorValue, 0, 1023, 255, 0);
    
  Serial.print("outputValue = ");
  Serial.print(outputValue);
  Serial.print("\t time = ");
  timeelapsed=micros()-prevtime;
  Serial.println(timeelapsed);
  prevtime=micros();
}
