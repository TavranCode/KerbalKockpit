void setup() {
  int c_first_input_pin1 = A8;
  int c_last_input_pin1 = A8;
  
  for (int i = c_first_input_pin1; i <= c_last_input_pin1; i++) {
    pinMode(i, INPUT);
  }
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(9600);
}

void loop() {
  Serial.print(0);
  Serial.print(" ");
  //Serial.print(analogRead(A0));
  //Serial.print(" ");
  //Serial.print(analogRead(A7));
  //Serial.print(" ");
  Serial.print(analogRead(A8));
  Serial.print(" ");
  Serial.println(1023);
  delay(10);
}
