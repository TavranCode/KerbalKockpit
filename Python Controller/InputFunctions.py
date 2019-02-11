import krpc

from Utilities import is_set, map_flt_ctl
import Settings


 #def SAS_inputs(input_buffer, vessel, mQ):
    # elif is_set(input_buffer[9], 2) != is_set(input_buffer_prev[9], 2):
        # vessel.control.sas = is_set(input_buffer[9], 2)

    # # need to handle exceptions here, not all modes are available at all times.
    # if is_set(input_buffer[9], 1) and not is_set(input_buffer_prev[9], 1):  # SAS Set requested
        # if is_set(input_buffer[8], 0):
            # try:
                # vessel.control.sas_mode = vessel.control.sas_mode.maneuver
            # except krpc.client.RPCError:
                # mQ.put((1, 'Could not set SAS Mode - Maneuver'))
                # pass
        # elif is_set(input_buffer[8], 1):
            # try:
                # vessel.control.sas_mode = vessel.control.sas_mode.anti_target
            # except krpc.client.RPCError:
                # mQ.put((1, 'Could not set SAS Mode - Anti-Target'))
                # pass
        # elif is_set(input_buffer[8], 2):
            # try:
                # vessel.control.sas_mode = vessel.control.sas_mode.target
            # except krpc.client.RPCError:
                # mQ.put((1, 'Could not set SAS Mode - Target'))
                # pass
        # elif is_set(input_buffer[8], 3):
            # try:
                # vessel.control.sas_mode = vessel.control.sas_mode.anti_radial
            # except krpc.client.RPCError:
                # mQ.put((1, 'Could not set SAS Mode - Anti-Radial'))
                # pass
        # elif is_set(input_buffer[8], 4):
            # try:
                # vessel.control.sas_mode = vessel.control.sas_mode.radial
            # except krpc.client.RPCError:
                # mQ.put((1, 'ould not set SAS Mode - Radial'))
                # pass
        # elif is_set(input_buffer[8], 5):
            # try:
                # vessel.control.sas_mode = vessel.control.sas_mode.anti_normal
            # except krpc.client.RPCError:
                # mQ.put((1, 'Could not set SAS Mode - Anti-Normal'))
                # pass
        # elif is_set(input_buffer[8], 6):
            # try:
                # vessel.control.sas_mode = vessel.control.sas_mode.normal
            # except krpc.client.RPCError:
                # mQ.put((1, 'Could not set SAS Mode - Normal'))
                # pass
        # elif is_set(input_buffer[8], 7):
            # try:
                # vessel.control.sas_mode = vessel.control.sas_mode.retrograde
            # except krpc.client.RPCError:
                # mQ.put((1, 'Could not set SAS Mode - Retrograde'))
                # pass
        # elif is_set(input_buffer[9], 0):
            # try:
                # vessel.control.sas_mode = vessel.control.sas_mode.prograde
            # except krpc.client.RPCError:
                # mQ.put((1, 'Could not set SAS Mode - Prograde'))
                # pass
        # else:
            # try:
                # vessel.control.sas_mode = vessel.control.sas_mode.stability_assist
            # except krpc.client.RPCError:
                # mQ.put((1, 'Error: Could not set SAS Mode - Stability Assist'))
                # pass

def flight_control_inputs(input_buffer, vessel, trim, thr_inhib, mQ):
    x_fctl_fine = 1
    trim[0] = 0
    trim[1] = 0
    trim[2] = 0
    pitch = map_flt_ctl(input_buffer[21], Settings.c_fctl_db, trim[0], x_fctl_fine)
    yaw = map_flt_ctl(input_buffer[20], Settings.c_fctl_db, trim[1], x_fctl_fine)
    roll = map_flt_ctl(input_buffer[22], Settings.c_fctl_db, trim[2], x_fctl_fine)
    
    vessel.control.pitch = pitch
    vessel.control.yaw = yaw
    vessel.control.roll = roll
    
    #mQ.put((0,'Running flight control'))
    # Throttle
    throttle_mode = 1
    # if is_set(input_buffer[9], 3):
        # throttle_mode = 1
    # if is_set(input_buffer[9], 4):
        # throttle_mode = 0.75
    # if is_set(input_buffer[9], 5):
        # throttle_mode = 0.5
    # if is_set(input_buffer[9], 6):
        # throttle_mode = 0.25

    #if not thr_inhib:
        # if is_set(input_buffer[7], 3):  # ROVER FC Mode - throttle used to set steady fwd power but stick overrides.
            # if vessel.control.wheel_throttle >= 0:
                # vessel.control.wheel_throttle = max(vessel.control.wheel_throttle, input_buffer[26] / 255 * throttle_mode)
            # vessel.control.throttle = 0
        # else:
            # vessel.control.wheel_throttle = 0
            
    throttletarget = input_buffer[26] / 255 * throttle_mode
    vessel.control.throttle = throttletarget
    #return throttletarget

    # return if controls in use so SAS can be overidden
    return (abs(pitch + abs(roll) + abs(yaw))) != 0