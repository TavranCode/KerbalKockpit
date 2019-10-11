void setup() {
  // put your setup code here, to run once:
  pinMode(2, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  analogWrite(2, HIGH);
  delay(2000);
  analogWrite(2, 125);
  delay(2000);
  analogWrite(2, 0);
  delay(2000);
}
