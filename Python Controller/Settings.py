from multiprocessing import Queue, Array
import ctypes


# SETUP CONSTANTS
c_camera_angle_rate = 1
c_camera_dist_rate = 1
c_camera_map_dist_rate = 10
c_trim_mod_rate = 0.01
c_fctl_db = 0.1
c_fctl_fine = 0.5
c_loop_frame_rate = 0.06
c_cam_change_time = 3.0




G_cam_change_timer = -1.0

msg_prefix = ("MSG", "ERROR", "CRITICAL ERROR")