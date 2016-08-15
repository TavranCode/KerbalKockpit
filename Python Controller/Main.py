from multiprocessing import Process, Queue, Array
from tkinter import Tk
import ctypes
from time import sleep
from Settings import *


from GUI import Application

# Define the shared data between the processes
msgQ = Queue(0)
data_array = Array(ctypes.c_ubyte, 50)

if __name__ == '__main__':
    # Create the root window
    root = Tk()
    root.title('KSP Controller')
    root.geometry('{0}x{1}'.format(c_screen_size_x,c_screen_size_y) + c_screen_pos)

    # Instatiate the GUI
    app = Application(root, data_array, msgQ)

    # Loop the window, calling an update then refreshing the window
    while 1:
        if app.game_connected == False or app.vessel_connected == False:
            app.connect(msgQ)
        else:
            app.update(data_array, msgQ)
        root.update()
        root.update_idletasks()
        sleep(0.1)
