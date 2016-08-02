from tkinter import *
from tkinter import ttk

from Utilities import is_set
from Settings import msg_prefix

class Application:

    global msg_prefix

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

        # Tab 9 - Maintenance
        # Tab 9 --> Left Frame - Arduino Data
        self.T9L = ttk.LabelFrame(tab9, text='Arduino Data', width=450, height=550)

        # Tab 9 --> Left Frame --> Sub Frames
        T9L_SD = ttk.LabelFrame(self.T9L, text='Status Data', width=420, height=150).grid(columnspan=2)
        self.T9L_DI = ttk.LabelFrame(self.T9L, text='Digital Inputs', width=200, height=300)
        self.T9L_AI = ttk.LabelFrame(self.T9L, text='Analogue Inputs', width=200, height=300)

        # Tab 9 - Left Frame --> Arduino Data --> Status Data

        # Tab 9 - Left Frame --> Arduino Data --> Digital Data
        ttk.Label(self.T9L_DI, text="Pins 8-10:").grid(column=0, row=0, sticky=(E))
        ttk.Label(self.T9L_DI, text="Pins 22-29:").grid(column=0, row=1, sticky=(E))
        ttk.Label(self.T9L_DI, text="Pins 30-37:").grid(column=0, row=2, sticky=(E))
        ttk.Label(self.T9L_DI, text="Pins 38-45:").grid(column=0, row=3, sticky=(E))
        ttk.Label(self.T9L_DI, text="Pins 46-53:").grid(column=0, row=4, sticky=(E))
        ttk.Label(self.T9L_DI, text="MUX 0 Bank A:").grid(column=0, row=5, sticky=(E))
        ttk.Label(self.T9L_DI, text="MUX 0 Bank B:").grid(column=0, row=6, sticky=(E))
        ttk.Label(self.T9L_DI, text="MUX 1 Bank A:").grid(column=0, row=7, sticky=(E))
        ttk.Label(self.T9L_DI, text="MUX 1 Bank B:").grid(column=0, row=8, sticky=(E))
        ttk.Label(self.T9L_DI, text="MUX 2 Bank B:").grid(column=0, row=9, sticky=(E))
        ttk.Label(self.T9L_DI, text="MUX 3 Bank B:").grid(column=0, row=10, sticky=(E))
        ttk.Label(self.T9L_DI, text="MUX 4 Bank B:").grid(column=0, row=11, sticky=(E))

        self.T9L_DI_01 = StringVar()
        self.T9L_DI_02 = StringVar()
        self.T9L_DI_03 = StringVar()
        self.T9L_DI_04 = StringVar()
        self.T9L_DI_05 = StringVar()
        self.T9L_DI_06 = StringVar()
        self.T9L_DI_07 = StringVar()
        self.T9L_DI_08 = StringVar()
        self.T9L_DI_09 = StringVar()
        self.T9L_DI_10 = StringVar()
        self.T9L_DI_11 = StringVar()
        self.T9L_DI_12 = StringVar()

        ttk.Label(self.T9L_DI, textvariable=self.T9L_DI_01).grid(column=1, row=0)
        ttk.Label(self.T9L_DI, textvariable=self.T9L_DI_02).grid(column=1, row=1)
        ttk.Label(self.T9L_DI, textvariable=self.T9L_DI_03).grid(column=1, row=2)
        ttk.Label(self.T9L_DI, textvariable=self.T9L_DI_04).grid(column=1, row=3)
        ttk.Label(self.T9L_DI, textvariable=self.T9L_DI_05).grid(column=1, row=4)
        ttk.Label(self.T9L_DI, textvariable=self.T9L_DI_06).grid(column=1, row=5)
        ttk.Label(self.T9L_DI, textvariable=self.T9L_DI_07).grid(column=1, row=6)
        ttk.Label(self.T9L_DI, textvariable=self.T9L_DI_08).grid(column=1, row=7)
        ttk.Label(self.T9L_DI, textvariable=self.T9L_DI_09).grid(column=1, row=8)
        ttk.Label(self.T9L_DI, textvariable=self.T9L_DI_10).grid(column=1, row=9)
        ttk.Label(self.T9L_DI, textvariable=self.T9L_DI_11).grid(column=1, row=10)
        ttk.Label(self.T9L_DI, textvariable=self.T9L_DI_12).grid(column=1, row=11)

        self.T9L_DI.grid(row=1, column=0)
        self.T9L_DI.grid_propagate(False)

        # Tab 9 - Left Frame --> Arduino Data --> Analogue Data
        ttk.Label(self.T9L_AI, text="Rotation X:").grid(column=0, row=0, sticky=(E))
        ttk.Label(self.T9L_AI, text="Rotation Y:").grid(column=0, row=1, sticky=(E))
        ttk.Label(self.T9L_AI, text="Rotation Z:").grid(column=0, row=2, sticky=(E))
        ttk.Label(self.T9L_AI, text="Translation X:").grid(column=0, row=3, sticky=(E))
        ttk.Label(self.T9L_AI, text="Translation Y:").grid(column=0, row=4, sticky=(E))
        ttk.Label(self.T9L_AI, text="Translation Z:").grid(column=0, row=5, sticky=(E))
        ttk.Label(self.T9L_AI, text="Throttle:").grid(column=0, row=6, sticky=(E))

        self.T9L_AI_01 = IntVar()
        self.T9L_AI_02 = IntVar()
        self.T9L_AI_03 = IntVar()
        self.T9L_AI_04 = IntVar()
        self.T9L_AI_05 = IntVar()
        self.T9L_AI_06 = IntVar()
        self.T9L_AI_07 = IntVar()

        ttk.Label(self.T9L_AI, textvariable=self.T9L_AI_01).grid(column=1, row=0)
        ttk.Label(self.T9L_AI, textvariable=self.T9L_AI_02).grid(column=1, row=1)
        ttk.Label(self.T9L_AI, textvariable=self.T9L_AI_03).grid(column=1, row=2)
        ttk.Label(self.T9L_AI, textvariable=self.T9L_AI_04).grid(column=1, row=3)
        ttk.Label(self.T9L_AI, textvariable=self.T9L_AI_05).grid(column=1, row=4)
        ttk.Label(self.T9L_AI, textvariable=self.T9L_AI_06).grid(column=1, row=5)
        ttk.Label(self.T9L_AI, textvariable=self.T9L_AI_07).grid(column=1, row=6)

        self.T9L_AI.grid(row=1, column=1)
        self.T9L_AI.grid_propagate(False)

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

        self.msgframe.grid(sticky=(E), padx=5, pady=5)
        self.msgframe.grid_propagate(False)

        # Buttons
        Button(lowerframe, text='Exit', command=root.destroy).grid(column=1, row=0)

        # Once the lower area is complete, grid it in
        lowerframe.grid(row=1, sticky=(E, W))

        # Finally grid the main frame into the root window
        mainframe.grid(column=0, row=0)


    def connect(self):
        pass

        # global spd
        # global ut, altitude, apoapsis, periapsis, eccentricity
        # conn = krpc.connect(name='Game Controller')
        # vessel = conn.space_center.active_vessel
        # spd = conn.add_stream(getattr, vessel.flight(vessel.orbit.body.reference_frame), 'speed')
        # ut = conn.add_stream(getattr, conn.space_center, 'ut')
        # altitude = conn.add_stream(getattr, vessel.flight(), 'mean_altitude')
        # apoapsis = conn.add_stream(getattr, vessel.orbit, 'apoapsis_altitude')
        # periapsis = conn.add_stream(getattr, vessel.orbit, 'periapsis_altitude')
        # eccentricity = conn.add_stream(getattr, vessel.orbit, 'eccentricity')

    def update(self, root, data_array, msgQ):
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

        # Tab 9 - Maintanance
        #Tab 9 --> Left Frame

        #Tab 9 --> Left Frame --> Digital Data Subframe
        self.T9L_DI_01.set('{0:08b}'.format(data_array[1]))
        self.T9L_DI_02.set('{0:08b}'.format(data_array[2]))
        self.T9L_DI_03.set('{0:08b}'.format(data_array[3]))
        self.T9L_DI_04.set('{0:08b}'.format(data_array[4]))
        self.T9L_DI_05.set('{0:08b}'.format(data_array[5]))
        self.T9L_DI_06.set('{0:08b}'.format(data_array[6]))
        self.T9L_DI_07.set('{0:08b}'.format(data_array[7]))
        self.T9L_DI_08.set('{0:08b}'.format(data_array[8]))
        self.T9L_DI_09.set('{0:08b}'.format(data_array[9]))
        self.T9L_DI_10.set('{0:08b}'.format(data_array[10]))
        self.T9L_DI_11.set('{0:08b}'.format(data_array[11]))
        self.T9L_DI_12.set('{0:08b}'.format(data_array[12]))

        #Tab 9 --> Left Frame --> Analogure Data Subframe
        self.T9L_AI_01.set(data_array[16])
        self.T9L_AI_02.set(data_array[17])
        self.T9L_AI_03.set(data_array[18])
        self.T9L_AI_04.set(data_array[19])
        self.T9L_AI_05.set(data_array[20])
        self.T9L_AI_06.set(data_array[21])
        self.T9L_AI_07.set(data_array[22])

        # Update message area
        if not msgQ.empty():
            m = msgQ.get()
            self.msgL1.set(self.msgL2.get())
            self.msgL2.set(self.msgL3.get())
            self.msgL3.set(self.msgL4.get())
            self.msgL4.set(msg_prefix[m[0]] + ": " + m[1])



