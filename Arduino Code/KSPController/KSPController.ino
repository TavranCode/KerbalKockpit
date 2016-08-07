
#include <Wire.h>
#include "KSPController.h"
#include "utils.h"

/* start code */
void setup() {
  /* set the PWM frequency on pin 6 to avoid fan whine */
  TCCR4B &= ~(B00000111);   /* set the three bits in TCCR2B to 0 */
  TCCR4B |= B00000001;      /* set the last three bits in TCCR2B with our new value, 1 is max freq */
  
  /* setup the digital output pins */
  for (i = c_first_output_pin; i <= c_last_output_pin; i++) {pinMode(i, OUTPUT);}

  /* turn on all the lights during the start up for a BIT check */
  digitalWrite(c_power_led_pin,HIGH);
  digitalWrite(c_error_led_pin,HIGH);
  digitalWrite(c_overrun_led_pin,HIGH);
  
  /* setup the digital input pins to activate internal pullup resistors*/
  for (i = c_first_input_pin1; i <= c_last_input_pin1; i++) {pinMode(i, INPUT_PULLUP);}
  for (i = c_first_input_pin2; i <= c_last_input_pin2; i++) {pinMode(i, INPUT_PULLUP);}

  /* set unused analogue input pins as digital outs forced low to prevent noise */
  for (i = A10; i <= A15; i++) {
    pinMode(i, OUTPUT);
    digitalWrite(i,LOW);
  }
  
  /* wake up the I2C_bus */
  Wire.begin(); 
 
  /* check we have all the MCP23017 chips */
  for (byte a = c_first_mux_address; a < c_last_mux_address; a++)   /* chip addresses start at 0x20, max of 8 chips */
  {
    Wire.beginTransmission (a);
    if (Wire.endTransmission () == 0) {n_mux_chips_detected++;} 
  } 
  if(n_mux_chips_detected != c_num_mux_chips) {sys_error(c_error_code_mux_missing);}

  /* setup the MUX output lines - MUX pins default to input on start up */
  mux_Tx(0x23, 0x00, 0x00);  /* MUX 0x23, IODIRA, Set all to output (0) */
  mux_Tx(0x23, 0x01, B11111110);  /* MUX 0x23, IODIRB, Set only pin 1 to output (0) */
  mux_Tx(0x24, 0x00, 0x00);  /* MUX 0x24, IODIRA, Set all to output (0) */
  mux_Tx(0x24, 0x01, B11111110);  /* MUX 0x24, IODIRB, Set only pin 1 to output (0) */

  /* reverse the polarity for all pins except the stage switch (which is already reversed) */
  mux_Tx(0x20,0x02, 0xFF);      /* Mux 0x20, IPOLA, Set All to reverse */
  mux_Tx(0x20,0x03, B01111111); /* Mux 0x20, IPOLB, Set All but pin B7 (stage sw) to reverse */
  mux_Tx(0x21,0x02, 0xFF);      /* Mux 0x21, IPOLA, Set All to reverse */
  mux_Tx(0x21,0x03, 0xFF);      /* Mux 0x21, IPOLB, Set All to reverse */
  mux_Tx(0x22,0x03, 0xFF);      /* Mux 0x22, IPOLB, Set All to reverse */
  mux_Tx(0x23,0x03, B11111110); /* Mux 0x23, IPOLB, Set All but pin B1 (output) to reverse */
  mux_Tx(0x24,0x03, B11111110); /* Mux 0x23, IPOLB, Set All but pin B1 (output) to reverse */
  
  /* start serial comms */
  Serial.begin(c_serial_speed);

  /* hold to allow light BIT to be seen */
  delay(c_light_bit_time);
  digitalWrite(c_power_led_pin,LOW);
  digitalWrite(c_error_led_pin,LOW);
  digitalWrite(c_overrun_led_pin,LOW);
}

/* main code loop */
void loop() {
  /* work out if we are ready for the next frame. As this is real time we need to allow 
   * for the processing time and run a fixed start delay 
   */        
        
   t_current_frame = millis();  /* frame start time */
   t_frame_time = t_current_frame - t_last_frame;  /* time since last frame */
   t_run_time = t_current_frame - t_power_on; /* keep track of time since power on */
        
   if(t_frame_time >= c_frame_time_target){ /* its time to run */
      t_last_frame = t_current_frame;  

      /* check if data received, if so read it in */
      if(Serial.available() == sizeof(x_inputbuffer)){
        Serial.readBytes(x_inputbuffer,sizeof(x_inputbuffer));
        if(x_inputbuffer[0] == 0x00){f_data_requested = TRUE;}
        else if(x_inputbuffer[0] == 0x01){f_data_received = TRUE;}
        t_last_serial_time = 0;
      }
      else{
        t_last_serial_time += t_frame_time;
      }
      
      /* check the input power */  
      if(analogRead(A0) < c_voltage_threshold){ 
         /* powered by USB only, flash the power light and do nothing else */
         light_flash(c_power_led_pin, &t_power_light, c_power_light_flash);
         /* turn off the error light, if it was flashing on when power was switch off it stays on! */
           digitalWrite(c_error_led_pin,LOW);
         f_power_on_first_pass = TRUE;
         t_run_time = 0;
         x_databuffer[0] = B00000001; /* set the status byte to 1 to alive (bit 1) but unpowered (bit 2)*/
         
      }
      else{ /* power is on, run the main program */
        if (f_power_on_first_pass ) {
              digitalWrite(c_power_led_pin,HIGH);  /* turn on the power light */
              t_power_on = t_current_frame;
              f_power_on_first_pass = FALSE;
           }
           
        if (t_last_serial_time >= c_serial_timeout) {
          /* no data from the main program, turn off all the lights and flash the error light */
          mux_Tx(0x23, 0x12, 0x00);  /* MUX 0x23, GPIOA */
          mux_Tx(0x23, 0x13, 0x00);  /* MUX 0x23, GPIOB */
          mux_Tx(0x24, 0x12, 0x00);  /* MUX 0x24, GPIOA */
          mux_Tx(0x24, 0x13, 0x00);  /* MUX 0x24, GPIOB */
          light_flash(c_error_led_pin, &t_error_light, c_error_light_flash);
        }
        else { /* serial hasn't timed out, proceed as normal */
           /* turn off the error light, if it was flashing on when serial started it stays on! */
           digitalWrite(c_error_led_pin,LOW);
           
           /* set the status byte */
           x_databuffer[0] = B00000011; /* bit 1 is true (alive) and bit 2 is true (powered) */ 
                    
           /* read all the inputs into the databuffer */
           read_inputs(&x_databuffer[1]);
  
           /* write the outputs to the lights  */
           if (f_data_received){
            write_outputs(x_inputbuffer, x_databuffer);
            f_data_received = FALSE;
           }
        
           /* set the dimmer value */
           analogWrite(c_dimmer_pwm_pin,x_databuffer[15]);
        }

        /* manage the fan */
        if (t_run_time < c_fan_power_up_time) { /* max speed initially to ensure it starts */
          analogWrite(c_fan_pwm_pin,255);
        }
        else { /* map fan speed to temp v fan speed curve */
          analogWrite(c_fan_pwm_pin,x_databuffer[14]*c_fan_speed_m+c_fan_speed_b);
        }

        /* check for high temp */
        if (x_databuffer[14] > c_temp_max) {sys_error(c_overtemp_error_code);}
        
        /* measure the processing time, signal if an overun occurs. add actual frame time to data buffer */
        t_frame_actual = millis() - t_current_frame;
        light_hold(t_frame_actual >= c_frame_time_target, c_overrun_led_pin, &t_overun_light, c_overun_lt_time);
        x_databuffer[23] = t_frame_actual;
  
        /* if data was requested, send data back */
        if(f_data_requested) {
          Serial.write(x_databuffer,sizeof(x_databuffer));
          f_data_requested = FALSE;
        }
      } /* end of 'if power on' condition */
   } /* end of 'if frame time reached' condition */
}

int read_inputs(byte buff[]){
/* this function reads in all digital inputs and places them in the data buffer */
      /* first clear the data buffer in the area we will do bit setting */
      for (i = 0; i < 5; i++) {
         buff[i] = 0;
      }

      /* read and map in the direct digital IO pins */
      for (i = c_first_input_pin1; i <= c_last_input_pin1; i++) {
        bitWrite(buff[0], (i-c_first_input_pin1)% 8, !digitalRead(i));
      }
      
      for (i = c_first_input_pin2; i <= c_last_input_pin2; i++) {
        bitWrite(buff[(i-c_first_input_pin2)/8 + 1], (i-c_first_input_pin2)% 8, !digitalRead(i));
      }

      /* now read the digital ins from each MUX bank.
       *  note that they already come as bytes so they can be copied straight in.
       */
      mux_Rx(0x20, 0x12, 1, &buff[5]);  
      mux_Rx(0x20, 0x13, 1, &buff[6]);  
      mux_Rx(0x21, 0x12, 1, &buff[7]);  
      mux_Rx(0x21, 0x13, 1, &buff[8]);  
      mux_Rx(0x22, 0x13, 1, &buff[9]);  
      mux_Rx(0x23, 0x13, 1, &buff[10]);  
      mux_Rx(0x24, 0x13, 1, &buff[11]);  

      /* read the analog inputs and map to a byte */
      buff[12] = map(analogRead(A0),0,1023,0,255);  /* Voltage sensor */
      buff[13] = map(analogRead(A1),0,1023,0,255);  /* Temperature Sensor */
      buff[14] = map(analogRead(A2),0,1023,255,2);  /* Dimmer - REVERSED - set a minimum to avoid no lights */
      buff[15] = map(analogRead(A3),0,1023,0,255);  /* Rotation X */
      buff[16] = map(analogRead(A4),0,1023,0,255);  /* Rotation Y */
      buff[17] = map(analogRead(A5),0,1023,0,255);  /* Rotation Z */
      buff[18] = map(analogRead(A6),0,1023,255,0);  /* Translation X - REVERSED */
      buff[19] = map(analogRead(A7),0,1023,0,255);  /* Translation Y */
      buff[20] = map(analogRead(A8),0,1023,0,255);  /* Translation Z */
      buff[21] = map(analogRead(A9),0,1023,0,255);  /* Throttle */
      return 0;       
}

int write_outputs(byte inputs[], byte outputs[]){
  byte temp = 0;
  /* start by mapping in the input data, then overwrite with locally driven lights from the output buffer*/
  temp = inputs[1]; /*shortcut to map in bits 0-3 */
  bitWrite(temp,4,bitRead(outputs[9],7));  /* staging armed */
  bitWrite(temp,5, (bitRead(outputs[9],3) || bitRead(outputs[9],4) || bitRead(outputs[9],5) || bitRead(outputs[9],6)));/* throttle armed */
  bitWrite(temp,6,(bitRead(outputs[9],4) || bitRead(outputs[9],5) || bitRead(outputs[9],6)));  /* throttle limited */
  bitWrite(temp,7,bitRead(outputs[9],2)); /* SAS Power On */
  mux_Tx(0x23, 0x12, temp);  /* MUX 0x23, GPIOA */

  temp = 0; /* we are not receiving anything here */
  bitWrite(temp,0,bitRead(outputs[7],6));  /* Controls Fine */
  mux_Tx(0x23, 0x13, temp);  /* MUX 0x23, GPIOB */

  temp = inputs[2]; /* shortcut to map in bits 0-3 and 5. Bit 4 will be overwritten later*/

  /* output 5 is the gear indicator. It should be on if gear is down (inputs[2] bit 5 is true), off
   *  if down(inputs[2] bit 4 is true) and flashing otherwise
   */
  if (!(bitRead(inputs[2],4)|| bitRead(inputs[2],5))) {
    t_gear_flash_timer += t_frame_time;
    bitWrite(temp,5,int(t_gear_flash_timer/c_gear_light_flash)%2); 
  }
  else{
    t_gear_flash_timer = 0;
  }
  bitWrite(temp,4,bitRead(outputs[11],3));  /* NWS armed */
  bitWrite(temp,6,(bitRead(outputs[11],5) || bitRead(outputs[11],6)));  /* Brakes */
  bitWrite(temp,7,bitRead(outputs[11],1));   /* Lights */
  mux_Tx(0x24, 0x12, temp);  /* MUX 0x24, GPIOA */

  temp = 0; /* we are not receiving anything here */
  bitWrite(temp,0,bitRead(outputs[11],2));  /* Controls Fine */
  mux_Tx(0x24, 0x13, temp);  /* MUX 0x24, GPIOB */
}
       
