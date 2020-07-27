/* Definitions */
#define TRUE 1
#define FALSE 0
//#define DEBUG               /* This flag will enable debug code */

/* Pin Assignments */
/* Analog Multiplex Vars */
const int p.selectPins[3] = {15, 16, 14}; // S0~2, S1~3, S2~4
const int p.zinput = A0; 
/* I2C */
const int p.scl = 4;
const int p.sda = 3;
/* PWM output */
const int p.Dim = 11;
const int p.bDim = 10;
const int p.motc = 9;
const int p.powerled = 5;
const int p.errled = A7;
/* Misc */
const int p.qsav = 13;
const int p.stagearm = p.Qsav; /*Qsav on schematic, arming in practice*/
const int p.qload = 12;
const int p.abortarm = p.Qload;

/* Pin Ranges */
const int outputs[10] = {5,A7,9,10,11,12,13,14,15,16};
const int inputs[8] = {A0,A1,A2,A3,A4,A5,A6,A8};

/* Variables */
byte x_databuffer[40];                  /* byte buffer for managing outputs */
byte x_inputbuffer[3];                  /* byte bugger for managing inputs */
//char s_ap_text1[41];                    /* AP panel message text line 1*/
//char s_ap_text2[41];                    /* AP panel message text line 2*/
//char s_ap_text_cons[3][13];             /* AP text constructor strings */
int f_data_received = 0;                /* data received flag */
int f_data_requested = 0;               /* data requested flag */
int i;                                  /* general loop counter */
int j;                                  /* general loop counter */
int n_mux_chips_detected = 0;           /* number of MUX chips detected in the IBIT */
int f_critical_error = 0;               /* critical error detected flag */
int f_power_on_first_pass = 1;          /* first pass flag when main power is turned on */
int x_dimmer_setting = 0;               /* dimmer setting */
int f_power_light_state = 0;            /* power light flash state */
int f_error_light_state = 0;            /* error light flash state */
int f_serial_state = 0;                 /* state of serial comm */

unsigned long t_power_light = 0;        /* timer for power light flashing calculation */
unsigned long t_overun_light = 0;       /* timer for overun light hold calculation */
unsigned long t_current_frame = 0;      /* current frame start time */
unsigned long t_frame_time = 0;         /* the simulation time for the current frame */
unsigned long t_last_frame = 0;         /* time since last frame */
unsigned long t_frame_actual = 0;       /* actual time it took to process the current frame */
unsigned long t_run_time = 0;           /* time since main power on */
unsigned long t_power_on = 0;           /* time when main power came on */
//unsigned long t_gear_flash_timer = 0;   /* timer for gear light flash calculation */
unsigned long t_last_serial_time = 0;   /* time since last serial data arrived */
unsigned long t_error_light = 100;        /* timer for error light flashing */

/* constants */
//const int c_power_light_flash = 1000;   /* power light flash rate [ms] */
//const int c_frame_time_target = 3;     /* target frame time [ms]*/
//const int c_gear_light_flash = 100;     /* gear light flash rate [ms]*/
const int c_light_bit_time = 1000;      /* time to delay to allow light BIT test to be seen [ms]*/
//const int c_serial_timeout = 5000;      /* serial timeout [ms]*/
//const int c_error_light_flash = 250;    /* no data flash rate for error light [ms]*/
  const byte add.matrix=0x20;      // I2C Address of matrix's MCP23017 chip
  const byte add.ledc=0x21; // I2C Address of LED Control MCP23017
  const byte IODIRA=0x00; // Register address of I/O configuration A
  const byte IODIRB=0x01; // Register address of I/O configuration B
  const byte GPIOA=0x12; // Register Address of Port A
  const byte GPIOB=0x13; // Register Address of Port B
  const byte qrows[8] = {0b11111110,0b11111101,0b11111011,0b11110111,0b11101111,0b11011111,0b10111111,0b01111111};

/* function prototypes*/
int read_inputs(byte buff[]);
int write_outputs(byte inputs[], byte outputs[]);
