void setup() {
  int c_first_input_pin1 = 2;
  int c_last_input_pin1 = 11;
  
  for (int i = c_first_input_pin1; i <= c_last_input_pin1; i++) {
    pinMode(i, INPUT);
  }
  pinMode(LED_BUILTIN, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(9600);
}

void loop() {
  int c_first_input_pin1 = 2;
  int c_last_input_pin1 = 11;

  String output = "Output: ";
  for (int i = c_first_input_pin1; i <= c_last_input_pin1; i++) {
    output.concat(i);
    output.concat(". ");
    output.concat(digitalRead(i));
    output.concat(" | ");
  }
    
  Serial.println(output);
  delay(100);
}

