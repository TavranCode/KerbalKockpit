void sys_error(void);
int light_flash(int pin, unsigned long *timer_prev, int flashtime);
int light_hold(int cond, int pin, unsigned long *timer, int holdtime);
int mux_Tx(int adr, int reg, byte data);
int mux_Rx(int adr, int reg, int numbytes, byte *data);

void sys_error(int code) {
  /* this function is called if a critical error exists. It flashes the error light as per the error code
   * and blocks all other functions 
   */
  while(true){
    for (int i = 0; i < code; i++){
      digitalWrite(c_error_led_pin,HIGH);
      delay(200);
      digitalWrite(c_error_led_pin,LOW);
      delay(200);
    }
    delay(1000);
  }
}

int light_flash(int pin, unsigned long *timer, int flashtime){
  /* this function will flash an output at the given time interval */
  *timer += t_frame_time;
  if (*timer > flashtime) { /* check for the timer to expire */
      *timer = 0; /* it has expired, reset the timer */
      digitalRead(pin) ? digitalWrite(pin,LOW): digitalWrite(pin,HIGH); /* set the pin to the opposite of whater it is now */
    }
  return 0;  /* should add a check to confirm pin is an output!! */
}

int light_hold(int cond, int pin, unsigned long *timer, int holdtime){
/* this function will hold the output true for the given time period when the input condition is met
 * Basically a delay off
 */
    if (cond) { *timer = holdtime; }
    if (*timer > 0 ) {
      digitalWrite(pin, HIGH);
      *timer -= max(*timer, t_frame_time); /* its an unsigned int, dont let it get < 0*/
    }
    else {
      digitalWrite(pin, LOW);
      *timer = 0;
    }
}

int mux_Tx(int adr, int reg, byte data) {
  /* This function will send data to a MCP23017 chip */
  Wire.beginTransmission(adr);     /* address the chip */
  Wire.write(reg);                 /* point to the register of choice */
  Wire.write(data);                /* send the data */
  Wire.endTransmission();          /* end the transmission */
  return 0;
}

int mux_Rx(int adr, int reg, int numbytes, byte *data){
  /* This function will request n bytes of data from a MCP23017 chip */
  Wire.beginTransmission(adr);     /* address the chip */
  Wire.write(reg);                 /* point to the register of choice */
  Wire.endTransmission();          /* end the transmission */
  Wire.requestFrom(adr,numbytes);  /* request the data */
  *data = Wire.read();
  return 0;
}

