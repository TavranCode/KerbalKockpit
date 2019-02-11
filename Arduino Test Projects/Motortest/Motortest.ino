
const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to
const int motorpin = 9;

int sensorValue = 0;        // value read from the pot
int outputValue;
int flip = 1;
// The pins to which we've wired each of the LEDs


void setup() {
    pinMode(9, OUTPUT);
    Serial.begin(9600);
}

void loop() {
  // read the analog in value:
  sensorValue = analogRead(analogInPin);
  // map it to a delay:
  outputValue = map(sensorValue, 0, 1023, 0, 1000);
  digitalWrite(motorpin,HIGH);
  delay(120);
  digitalWrite(motorpin,0);
  Serial.print("\t delay = ");
  Serial.println(outputValue);
  delay(outputValue);
}
