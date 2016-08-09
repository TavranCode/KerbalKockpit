from tkinter import *
from tkinter import ttk
import krpc

from Utilities import is_set, si_val
from Settings import msg_prefix


class Subframe:
    def __init__(self, root, title, labels, width, height):
        self.frame_name = ttk.LabelFrame(root, text=title, width=width, height=height)

        for i in range(len(labels)):
            ttk.Label(self.frame_name, text=labels[i]).grid(column=0, row=i, sticky=E)

        self.data_labels = []
        for i in range(len(labels)):
            self.data_labels.append(StringVar())
            ttk.Label(self.frame_name, textvariable=self.data_labels[i]).grid(column=1, row=i)

    def grid(self, row=0, column=0, columnspan=1):
        self.frame_name.grid(row=row, column=column, columnspan=columnspan)
        self.frame_name.grid_propagate(False)

    def update(self, value_strings):
        for i in range(len(value_strings)):
            self.data_labels[i].set(value_strings[i])


class Application:
    def __init__(self, root):

        mainframe = ttk.Frame(root)

        self.notebook = ttk.Notebook(mainframe, width=1014, height=600)

        tab1 = ttk.Frame(self.notebook)
        tab2 = ttk.Frame(self.notebook)
        tab3 = ttk.Frame(self.notebook)
        tab4 = ttk.Frame(self.notebook)
        tab5 = ttk.Frame(self.notebook)
        tab6 = ttk.Frame(self.notebook)
        tab7 = ttk.Frame(self.notebook)
        tab8 = ttk.Frame(self.notebook)
        tab9 = ttk.Frame(self.notebook)

        self.notebook.add(tab1, text='Launch')
        self.notebook.add(tab2, text='Orbital')
        self.notebook.add(tab3, text='Landing')
        self.notebook.add(tab4, text='Rondezvous')
        self.notebook.add(tab5, text='Flight')
        self.notebook.add(tab6, text='Runway')
        self.notebook.add(tab7, text='Rover')
        self.notebook.add(tab8, text='Systems')
        self.notebook.add(tab9, text='Maintenance')

        # Tab 2 - Orbital
        # Tab 9 --> Left Frame - Orbital Data
        self.T2L = ttk.LabelFrame(tab2, text='Orbital Data', width=450, height=550)

        # Tab 2 --> Left Frame --> Sub Frames
        self.T2L_OI = Subframe(self.T2L, 'Orbit Info', ('Orbital Speed:', 'Apoapsis:', 'Periapsis:', 'Orbital Period:',
                                                        'Time to Apoapsis:', 'Time to Periapsis:', 'Inclination:', 'Ecentricity:',
                                                        'Longitude of Ascending Node:'), 420, 300)
        self.T2L_OI.grid(row=0, column=0)

        self.T2L_VI = Subframe(self.T2L, 'Orbit Info', ('Vessel Mass:', 'Current TWR:'), 420, 150)
        self.T2L_VI.grid(row=1, column=0)

        self.T2L.grid()

        # Tab 9 - Maintenance
        # Tab 9 --> Left Frame - Arduino Data
        self.T9L = ttk.LabelFrame(tab9, text='Arduino Data', width=450, height=550)

        # Tab 9 --> Left Frame --> Sub Frames
        self.T9L_SD = Subframe(self.T9L, 'Status Data', ('Status Byte:', 'Frame Time:', 'Temperature:', 'Fan Speed:', 'Dimmer Setting:'), 420, 200)
        self.T9L_SD.grid(row=0, column=0, columnspan=2)

        self.T9L_DI = Subframe(self.T9L, 'Digital Inputs', ('Pins 8-10:', 'Pins 22-29:', 'Pins 30-37:', 'Pins 38-45:', 'Pins 46-53:', 'MUX 0 Bank A:',
                                                            'MUX 0 Bank B:', 'MUX 1 Bank A:', 'MUX 1 Bank B:', 'MUX 2 Bank B:', 'MUX 3 Bank B:',
                                                            'MUX 4 Bank B:'), 200, 300)
        self.T9L_DI.grid(row=1, column=0, )

        self.T9L_AI = Subframe(self.T9L, 'Analogue Inputs', ('Rotation X:', 'Rotation Y:', 'Rotation Z:', 'Translation X:', 'Translation Y:',
                                                             'Translation Z:', 'Throttle:'), 200, 300)
        self.T9L_AI.grid(row=1, column=1)

        self.T9L.grid()

        # Grid in the notebook once all content is done
        self.notebook.grid(column=0, row=0, padx=5, pady=5)

        # Build the lower area for the messages and buttons
        lowerframe = ttk.Frame(mainframe, width=1014, height=100)

        # Build the Message box with four data lines
        self.msgframe = ttk.LabelFrame(lowerframe, text='Status Messages', width=950, height=100)

        self.msgL1 = StringVar()
        self.msgL2 = StringVar()
        self.msgL3 = StringVar()
        self.msgL4 = StringVar()

        self.msg1 = ttk.Label(self.msgframe, textvariable=self.msgL1).grid(row=0, sticky=(E, W))
        self.msg2 = ttk.Label(self.msgframe, textvariable=self.msgL2).grid(row=1, sticky=(E, W))
        self.msg3 = ttk.Label(self.msgframe, textvariable=self.msgL3).grid(row=2, sticky=(E, W))
        self.msg4 = ttk.Label(self.msgframe, textvariable=self.msgL4).grid(row=3, sticky=(E, W))

        self.msgframe.grid(sticky=E, padx=5, pady=5)
        self.msgframe.grid_propagate(False)

        # Buttons
        Button(lowerframe, text='Exit', command=root.destroy).grid(column=1, row=0)

        # Once the lower area is complete, grid it in
        lowerframe.grid(row=1, sticky=(E, W))

        # Finally grid the main frame into the root window
        mainframe.grid(column=0, row=0)

    def connect(self):
        conn = krpc.connect(name='Game Controller GUI')
        vessel = conn.space_center.active_vessel
        spd = conn.add_stream(getattr, vessel.flight(vessel.orbit.body.reference_frame), 'speed')
        ut = conn.add_stream(getattr, conn.space_center, 'ut')
        altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')

        self.orbital_speed = conn.add_stream(getattr, vessel.orbit, 'speed')
        self.apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
        self.periapsis = conn.add_stream(getattr, vessel.orbit, 'periapsis_altitude')
        self.orbital_period = conn.add_stream(getattr, vessel.orbit, 'period')
        self.time_to_apoapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_apoapsis')
        self.time_to_periapsis = conn.add_stream(getattr, vessel.orbit, 'time_to_periapsis')
        self.inclination = conn.add_stream(getattr, vessel.orbit, 'inclination')
        self.eccentricity = conn.add_stream(getattr, vessel.orbit, 'eccentricity')
        self.long_asc_node = conn.add_stream(getattr, vessel.orbit, 'longitude_of_ascending_node')

    def update(self, data_array, msgQ):
        # Manage notebook tab switching
        if is_set(data_array[4], 6):
            self.notebook.select(7)
        elif is_set(data_array[5], 0):
            self.notebook.select(6)
        elif is_set(data_array[5], 2):
            self.notebook.select(5)
        elif is_set(data_array[5], 4):
            self.notebook.select(4)
        elif is_set(data_array[5], 6):
            self.notebook.select(3)
        elif is_set(data_array[2], 4):
            self.notebook.select(2)
        elif is_set(data_array[2], 6):
            self.notebook.select(1)
        elif is_set(data_array[3], 0):
            self.notebook.select(0)
        else:
            self.notebook.select(8)

        # Tab 2 - Maintanance
        # Tab 2 --> Left Frame
        # Tab 2 --> Left Frame --> Orbital Info Subframe

        temp = [si_val(self.orbital_speed()) + 'm/s',
                si_val(self.apoapsis()) + 'm',
                si_val(self.periapsis()) + 'm',
                '{0:.0f}s'.format(self.orbital_period()),
                '{0:.0f}s'.format(self.time_to_apoapsis()),
                '{0:.0f}s'.format(self.time_to_periapsis()),
                '{0:.2f} deg'.format(self.inclination()),
                '{0:.4f}'.format(self.eccentricity()),
                '{0:.2f} deg'.format(self.long_asc_node())]
        self.T2L_OI.update(temp)

        # Tab 9 - Maintanance
        # Tab 9 --> Left Frame
        # Tab 9 --> Left Frame --> Status Data Subframe
        temp = ['{0:08b}'.format(data_array[0]),
                '{:d}ms'.format(data_array[23]),
                '{0:.0f}deg'.format(data_array[14] * 0.69310345 - 68.0241379),
                '{0:.0f}%'.format(data_array[24] / 255 * 100),
                '{0:.0f}%'.format(data_array[15] / 255 * 100)]

        self.T9L_SD.update(temp)

        # Tab 9 --> Left Frame --> Digital Data Subframe
        temp = ['{0:08b}'.format(data_array[1]),
                '{0:08b}'.format(data_array[2]),
                '{0:08b}'.format(data_array[3]),
                '{0:08b}'.format(data_array[4]),
                '{0:08b}'.format(data_array[5]),
                '{0:08b}'.format(data_array[6]),
                '{0:08b}'.format(data_array[7]),
                '{0:08b}'.format(data_array[8]),
                '{0:08b}'.format(data_array[9]),
                '{0:08b}'.format(data_array[10]),
                '{0:08b}'.format(data_array[11]),
                '{0:08b}'.format(data_array[12])]
        self.T9L_DI.update(temp)

        # Tab 9 --> Left Frame --> Analogure Data Subframe
        temp = [data_array[16],
                data_array[17],
                data_array[18],
                data_array[19],
                data_array[20],
                data_array[21],
                data_array[22]]
        self.T9L_AI.update(temp)

        # Update message area
        if not msgQ.empty():
            m = msgQ.get()
            self.msgL1.set(self.msgL2.get())
            self.msgL2.set(self.msgL3.get())
            self.msgL3.set(self.msgL4.get())
            self.msgL4.set(msg_prefix[m[0]] + ': ' + m[1])
