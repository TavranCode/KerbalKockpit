#define ENCODER_DO_NOT_USE_INTERRUPTS
#include <Encoder.h>
Encoder myEnc(2, 3);

void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  Serial.println("Basic NoInterrupts Test:");
}

long position  = -999;

void loop() {
  // put your main code here, to run repeatedly:
  long newPos = myEnc.read();
  if (newPos != position) {
    position = newPos;
    Serial.println(position);
  }
  // With any substantial delay added, Encoder can only track
  // very slow motion.  You may uncomment this line to see
  // how badly a delay affects your encoder.
  delay(20);
}
