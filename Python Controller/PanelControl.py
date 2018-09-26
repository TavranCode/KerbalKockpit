import serial
import krpc
import time
import operator

import Settings
from Utilities import is_set, norm
from OutputFunctions import output_mapping
from InputFunctions import flight_control_inputs #SAS_inputs, camera_inputs
#from LandingGuidance import ldg_guidance_draw, ldg_guidance_clear
from CNIA import cnia
#from Autopilot import Autopilot


def panel_control(data_array, mQ):
    n_program_state = 1
    t_quickload_timer = 0
    t_frame_start_time = time.time()
    BA_input_buffer = bytearray()
    f_first_pass = 1
    x_trim = [0, 0, 0]
    throttle_inhib = False
    spd_err = 0
    spd_err_p = 0

    while 1:
        if time.time() - t_frame_start_time >= Settings.c_loop_frame_rate:
            # record the start of the processing so we can get timing data
            t_frame_start_time = time.time()

            # STATE = PANEL CONN - Connect to the panel
            if n_program_state == 1:
                mQ.put((0, 'Connecting to the panel....'))
                try:
                    ser = serial.Serial('./COM3', 9600, timeout=0.1)
                    mQ.put((0, 'Connected to the panel'))
                    time.sleep(1)  # serial needs a little bit of time to initialise, otherwise later code - esp CNIA fails
                    n_program_state = 2
                except serial.serialutil.SerialException:
                    mQ.put((1, 'Could not connect to the panel'))
                    time.sleep(5)  # to avoid spamming the message queue
                    pass

            # STATE = GAME CONN - Connect to the KRPC Server
            if n_program_state == 2:
                mQ.put((0, 'Connecting to the game server....'))
                try:
                    conn = krpc.connect(name='Game Controller')
                    mQ.put((0, 'Connected to the game server'))
                    n_program_state = 3
                except ConnectionRefusedError:
                    mQ.put((1, 'Could not connect to the game server'))
                    pass

            # STATE = LINKING - Link to the active Vessel
            if n_program_state == 3 and conn.krpc.current_game_scene == conn.krpc.current_game_scene.flight:
                mQ.put((0, 'Connecting to the vessel....'))
                try:
                    vessel = conn.space_center.active_vessel
                    mQ.put((0, 'Linked to ' + vessel.name))
                    n_program_state = 4
                except krpc.client.RPCError:
                    mQ.put((1, 'Could not connect to a vessel'))
                    pass

            # STATE = Perform CNIA
            if n_program_state == 4:
                mQ.put((0, 'Starting CNIA...'))
                raise TimeoutError("Out of function timeout")
                cnia(ser,conn,vessel)
                # try:
                    # cnia(ser, conn, vessel)
                # except TimeoutError:
                    # mq.put((1,'exception'))
                    # mq.put((1, ' '.join(err.args)))
                    # time.sleep(5)
                    # pass
                # except serial.serialutil.SerialException:
                    # mQ.put((1, 'CNIA could not connect to the panel'))
                    # time.sleep(5)  # to avoid spamming the message queue
                    # pass
                mQ.put((0, 'CNIA Complete'))
                n_program_state = 5

            # STATE = Streams and objects- setup data input streams and reused objects
            if n_program_state == 5:
                # Get SAS status
                mQ.put((0, 'Begin stream setup'))
                sas_stream = [conn.add_stream(getattr, vessel.control, 'sas')]
                mQ.put((0, 'Stream setup complete'))
                n_program_state = 6

            # STATE = RUNNING
            if n_program_state == 6:
                try:  # catch RPC errors as they generally result from a scene change. Make more specific KRPC issue 256
                    # Send data to the arduino request it to process inputs  - command byte = 0x00
                    BA_output_buffer = bytearray([0x00, 0x00, 0x00])
                    ser.write(BA_output_buffer)

                    # Now while the Arduino is busy with inputs we processes the outputs - command byte = 0x01
                    #BA_output_buffer = bytearray([0x01, 0x00, 0x00])
                    #output_mapping(BA_output_buffer, conn, sas_stream)

                    # Make sure the Arduino has responded
                    while ser.in_waiting != 40:
                        pass

                    # read back the data from the arduino
                    BA_input_buffer_prev = BA_input_buffer
                    BA_input_buffer = ser.read(40)

                    # Now send the output date we calculated earlier
                    # ser.write(BA_output_buffer)

                    if f_first_pass:  # On the first pass copy the data in to avoid an error.
                        BA_input_buffer_prev = BA_input_buffer
                        f_first_pass = 0
                    
                    # Check the status of the Arduino and make the controls work
                    #mQ.put((0,'input buffer is ' + BA_input_buffer[0]))
                    if BA_input_buffer[0] == 3:  # status of 00000011 is fully powered
                        #mQ.put((0,'starting input buffer statement'))
                        # SAS
                        #SAS_inputs(BA_input_buffer, BA_input_buffer_prev, vessel, mQ)
                        # Flight Control (currently just throttle)
                        try:
                            throttle_justset = flight_control_inputs(BA_input_buffer, vessel, throttle_inhib, mQ)
                        except Exception as e:
                            mQ.put((1,'flight control error'))
                            mQ.put((1,repr(e)))
                        # put all the data onto the shared array for use by the GUI
                        mQ.put((0,'ran flight control'))
                        for i in range(len(BA_input_buffer)):
                            data_array[i] = BA_input_buffer[i]
                        #mQ.put((0,'out of loop'))

                except krpc.client.RPCError:
                    n_program_state = 3
                    mQ.put((1, 'Main Loop Error'))

            # Check for Overuns and send a warning.
            if (time.time() - t_frame_start_time) > Settings.c_loop_frame_rate * 1.1:
                mQ.put((1, 'OVERUN - ' + str(int((time.time() - t_frame_start_time) * 1000)) + 'ms'))
