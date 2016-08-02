
#define TRUE 1
#define FALSE 0

/* Variables */
byte x_databuffer[24];                  /* byte buffer for managing outputs */
byte x_inputbuffer[3];                  /* byte bugger for managing inputs */
int f_data_received = 0;                /* data received flag */
int f_data_requested = 0;               /* data requested flag */
int i;                                  /* general loop counter */
unsigned long t_power_light = 0;        /* timer for power light flashing calculation */
unsigned long t_overun_light = 0;       /* timer for overun light hold calculation */
int n_mux_chips_detected = 0;           /* number of MUX chips detected in the IBIT */
int f_critical_error = 0;               /* critical error detected flag */
int f_power_on_first_pass = 1;          /* first pass flag when main power is turned on */
unsigned long t_current_frame = 0;      /* current frame start time */
unsigned long t_frame_time = 0;         /* the simulation time for the current frame */
unsigned long t_last_frame = 0;         /* time since last frame */
unsigned long t_frame_actual = 0;       /* actual time it took to process the current frame */
unsigned long t_run_time = 0;           /* time since main power on */
unsigned long t_power_on = 0;           /* time when main power came on */
unsigned long t_gear_flash_timer = 0;   /* timer for gear light flash calculation */
unsigned long t_last_serial_time = 0;   /* time since last serial data arrived */
unsigned long t_error_light = 0;        /* timer for error light flashing */

/* constants */
const int c_voltage_threshold = 600;    /* analog reading of the voltage sensor about which we know we are externally powered */
const int c_power_light_flash = 1000;   /* power light flash rate in millisec */
const int c_num_mux_chips = 5;          /* the number of MCP23017 chips installed */
const int c_first_input_pin1 = 8;       /* the first pin used for digital IO */
const int c_last_input_pin1 = 10;       /* the last input pin used for digital IO */
const int c_first_input_pin2 = 22;      /* the first pin used for digital IO */
const int c_last_input_pin2 = 54;       /* the last input pin used for digital IO */
const int c_first_output_pin = 2;       /* the first pin used for digital output */
const int c_last_output_pin = 6;        /* the last output pin used for digital IO */
const int c_error_code_mux_missing = 1; /* error code if MUX count is incorrect */
const int c_frame_time_target = 10;     /* target frame time in ms */
const int c_overun_lt_time = 100;       /* Overun Light hold time */
const int c_fan_power_up_time = 5000;   /* Time that fan will run full speed at start in ms */
const float c_fan_speed_m = 3.448;      /* fan speed vs temp slope */
const float c_fan_speed_b = -282.931;   /* fan speed vs temp Y intercept */
const int c_temp_max = 160;             /* overtemp limit, stop. Equates to about 3 degrees above max fan speed.  */
const int c_overtemp_error_code = 2;    /* error code if overtemp limit exceeded */
const int c_gear_light_flash = 500;     /* gear light flash rate in millisec */
const int c_first_mux_address = 32;     /* the first I2C address in the MUX range */
const int c_last_mux_address = 40;      /* the last I2C address in the MUX range */
const long c_serial_speed = 115200;     /* serial bus baud rate */
const int c_light_bit_time = 1000;      /* time to delay to allow light BIT test to be seen */
const int c_serial_timeout = 1000;      /* serial timeout */
const int c_error_light_flash = 250;    /* no data flash rate for error light */

/* pin mappings */
const int c_power_led_pin = 2;
const int c_error_led_pin = 3;
const int c_overrun_led_pin = 4;
const int c_dimmer_pwm_pin = 5;
const int c_fan_pwm_pin = 6;


/* function prototypes*/ 

int read_inputs(byte buff[]);
int write_outputs(byte inputs[], byte outputs[]);

