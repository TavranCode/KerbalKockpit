from multiprocessing import Process, Queue, Array
from tkinter import Tk
import ctypes
from time import sleep

from PanelControl import panel_control
from GUI import Application

# Define the shared data betweem the processes
msgQ = Queue(0)
data_array = Array(ctypes.c_ubyte, 50)

if __name__ == '__main__':
    # Start the panel controller module
    p = Process(target=panel_control, args=(data_array, msgQ))
    p.start()

    # Create the root window
    root = Tk()
    root.title('KSP Controller')
    root.geometry('1024x768+700-1000')

    # Instatiate the GUI
    app = Application(root)

    # Run the connection method
    app.connect()

    # Loop the window, calling an update then refreshing the window
    while 1:
        app.update(data_array, msgQ)
        root.update()
        root.update_idletasks()
        sleep(0.1)
