
const int analogInPin = A0;  // Analog input pin that the potentiometer is attached to

int sensorValue = 0;        // value read from the pot
int outputValue = 0;        // value output to the PWM (analog out)
int outputValuei = 0;       // value output to the PWM inverted

// The pins to which we've wired each of the LEDs
int ledPinsd[] = {2, 4, 7};
int ledPinsa[] = {3, 5, 6};
const int dimmerpin = 9;

// The number we're going to display.
byte count;
byte fcount;

const int on = 255;
const int off = 0;

void setup() {
{
  for (byte i = 0; i < 3; i++) {
    pinMode(ledPinsa[i], OUTPUT);
    pinMode(ledPinsd[i], OUTPUT);
  }
  count = 0;
  fcount = 0;
}
    Serial.begin(9600);
}

void loop() {
  // read the analog in value:
  sensorValue = analogRead(analogInPin);
  // map it to the range of the analog out:
  outputValue = map(sensorValue, 0, 1023, 255, 0);
  outputValuei = map(sensorValue, 0, 1023, 0, 255);
  // change the analog out value:
  // analogWrite(analogOutPin, outputValue);
  analogWrite(dimmerpin,outputValuei);
  if(fcount % 25 == 0) {
    count++;
  }
  
  if (count & 0b0000001) {
    analogWrite(ledPinsa[0],outputValue);
    digitalWrite(ledPinsd[0],on);
  } else {
    analogWrite(ledPinsa[0],on);
    digitalWrite(ledPinsd[0],off);
  }
  
  if (count & 0b0000010) {
    analogWrite(ledPinsa[1],outputValue);
    digitalWrite(ledPinsd[1],on);
  } else {
    analogWrite(ledPinsa[1],on);
    digitalWrite(ledPinsd[1],off);
  }
  
  if (count & 0b0000100) {
    analogWrite(ledPinsa[2],outputValue);
    digitalWrite(ledPinsd[2],on);
  } else {
    analogWrite(ledPinsa[2],on);
    digitalWrite(ledPinsd[2],off);
  }

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
