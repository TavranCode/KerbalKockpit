from tkinter import *
from tkinter import ttk
import krpc
from multiprocessing import Process
from math import degrees, pi
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

from Utilities import is_set, si_val, sec2time, SubframeLabel, SubframeVar, norm, bytes2int
from Settings import *
from PanelControl import panel_control



class Application:
    def __init__(self, root, data_array, msgQ):

        # Define Styles
        self.styles = ttk.Style()
        self.styles.configure('Display.TLabel', font=(defaultfont, '18'), padding=(10, 0), background='black', foreground=darkcolor)
        self.styles.configure('Msg.TLabel', font=(defaultfont, '10'), padding=(10, 0), background='black', foreground=darkcolor)
        self.styles.configure('Ind.TLabel', font=(defaultfont, '16', 'bold'), padding=(10, 0), relief='raised', anchor='center')
        self.styles.configure('TNotebook.Tab', font=(defaultfont, '14', 'bold'), padding=(10, 0))
        self.styles.configure('TLabelframe.Label', font=(defaultfont, '24', 'bold'), background='black',foreground=lightcolor)
        self.styles.configure('TLabelframe', background='black')
        self.styles.configure('TFrame', background='black')
        self.styles.configure('TButton', font=(defaultfont, '16', 'bold'))
        self.styles.configure('Ind.TLabel', font=(defaultfont, '16', 'bold'), padding=(10, 0), relief='raised', anchor='center')

        # Create the notebook and define its tabs
        self.notebook = ttk.Notebook(root)

        tab9 = ttk.Frame(self.notebook, borderwidth=10)

        self.notebook.add(tab9, text='Maintenance')

        # Tab 9 - Maintenance
        # Tab 9 --> Left Frame - Arduino Data
        self.T9L = ttk.Frame(tab9)
        self.T9R = ttk.Frame(tab9)

        self.T9_SD = SubframeLabel(self.T9L, 'Arduino Status', ('Status Byte:', 'Frame Time:', 'Temperature:', 'Fan Speed:', 'Dimmer:'))
        self.T9_SD.pack()

        self.T9_DI = SubframeLabel(self.T9L, 'Digital Inputs', ('Pins 8-9:', 'Pins 22-29:', 'Pins 30-37:', 'Pins 38-45:', 'Pins 46-53:', 'MUX 0 Bank A:',
                                                                'MUX 0 Bank B:', 'MUX 1 Bank A:', 'MUX 1 Bank B:', 'MUX 2 Bank B:', 'MUX 3 Bank B:',
                                                                'MUX 4 Bank B:', 'MUX 5 Bank A:', 'MUX 5 Bank B:', 'MUX 6 Bank B:', 'MUX 6 Bank B:'))
        self.T9_DI.pack()

        self.T9_AI = SubframeLabel(self.T9R, 'Analogue Inputs', ('Rotation X:', 'Rotation Y:', 'Rotation Z:', 'Translation X:', 'Translation Y:',
                                                                 'Translation Z:', 'Throttle:'))
        self.T9_AI.pack()

        self.T9L.pack(anchor=N, side=LEFT, expand=1, fill=X, padx=5)
        self.T9R.pack(anchor=N, side=RIGHT, expand=1, fill=X, padx=5)

        # Pack in the notebook once all content is done
        self.notebook.pack(expand=1, fill=BOTH)

        # Build the lower area for the messages and buttons
        lowerframe = ttk.Frame(root)

        # Build the Message box with four data lines
        self.msgframe = ttk.LabelFrame(lowerframe, text='Status Messages')

        self.msgL1 = StringVar()
        self.msgL2 = StringVar()
        self.msgL3 = StringVar()
        self.msgL4 = StringVar()

        self.msg1 = ttk.Label(self.msgframe, style='Msg.TLabel', textvariable=self.msgL1).pack(anchor=W)
        self.msg2 = ttk.Label(self.msgframe, style='Msg.TLabel', textvariable=self.msgL2).pack(anchor=W)
        self.msg3 = ttk.Label(self.msgframe, style='Msg.TLabel', textvariable=self.msgL3).pack(anchor=W)
        self.msg4 = ttk.Label(self.msgframe, style='Msg.TLabel', textvariable=self.msgL4).pack(anchor=W)

        self.msgframe.pack(side=LEFT, expand=1, fill=BOTH, padx=5, pady=5)

        # Buttons
        self.panel_status = StringVar()
        self.panel_status.set("Disconnected")

        self.buttonframe = ttk.LabelFrame(lowerframe, text='Controls')

        ttk.Button(self.buttonframe, text='Connect Panel', command=lambda: self.connect_panel(data_array, msgQ), width=15).grid(column=1, row=0, sticky=SE, padx=5, pady=3)
        ttk.Button(self.buttonframe, text='Disconnect Panel', command=self.disconnect_panel, width=15).grid(column=1, row=1, sticky=NE, padx=4, pady=3)
        self.panel_status_button = ttk.Label(self.buttonframe, textvariable=self.panel_status, width=13, style='Ind.TLabel', relief='raised').grid(column=2, row=0, sticky=(S, E, W), padx=4, pady=6)
        ttk.Button(self.buttonframe, text='Exit', command=lambda: self.exit(root), width=15).grid(column=2, row=1, sticky=NE, padx=5, pady=3)

        self.buttonframe.pack(side=RIGHT, fill=Y, padx=5, pady=5)

        # Once the lower area is complete, grid it in
        lowerframe.pack(expand=1, fill=BOTH, padx=5, pady=5)

        # Initialise connection attributes
        self.panel_proc = None
        self.conn = None
        self.vessel = None
        self.speed = None
        self.h_speed = None
        self.v_speed = None
        self.pitch = None
        self.roll = None
        self.heading = None
        self.agl_altitude = None
        self.orbital_speed = None
        self.apoapsis = None
        self.periapsis = None
        self.orbital_period = None
        self.time_to_apoapsis = None
        self.time_to_periapsis = None
        self.inclination = None
        self.eccentricity = None
        self.long_asc_node = None
        self.ecc_anomaly = None
        self.mass = None
        self.thrust = None
        self.max_thrust = None
        self.surface_gravity = None
        self.res_names = None
        self.res_streams = None
        self.resIDS_names = None
        self.resIDS_streams = None
        self.mean_altitude = None
        self.latitude = None
        self.longitude = None
        self.arg_periapsis = None

        # initialise attributes that require a state
        self.panel_connected = False
        self.game_connected = False
        self.vessel_connected = False
        self.notebook_page = 0

    def connect(self, mQ):
        mQ.put((0, 'GUI Connecting to the game server....'))
        if self.game_connected is False:
            try:
                self.conn = krpc.connect(name='Game Controller GUI')
                mQ.put((0, 'GUI Connected to the game server'))
                self.game_connected = True
            except ConnectionRefusedError:
                mQ.put((1, 'GUI Could not connect to the game server'))

        if self.game_connected and self.vessel_connected is False and self.conn.krpc.current_game_scene == self.conn.krpc.current_game_scene.flight:
            mQ.put((0, 'GUI Connecting to the vessel....'))
            try:
                self.vessel = self.conn.space_center.active_vessel
                mQ.put((0, 'GUI Linked to ' + self.vessel.name))
                self.vessel_connected = True
            except krpc.client.RPCError:
                mQ.put((1, 'GUI Could not connect to a vessel'))
                pass

        if self.vessel_connected:
            orbital_ref_frame = self.vessel.orbit.body.reference_frame
            self.speed = self.conn.add_stream(getattr, self.vessel.flight(orbital_ref_frame), 'speed')
            self.h_speed = self.conn.add_stream(getattr, self.vessel.flight(orbital_ref_frame), 'horizontal_speed')
            self.v_speed = self.conn.add_stream(getattr, self.vessel.flight(orbital_ref_frame), 'vertical_speed')
            self.pitch = self.conn.add_stream(getattr, self.vessel.flight(), 'pitch')
            self.roll = self.conn.add_stream(getattr, self.vessel.flight(), 'roll')
            self.heading = self.conn.add_stream(getattr, self.vessel.flight(), 'heading')
            self.agl_altitude = self.conn.add_stream(getattr, self.vessel.flight(), 'surface_altitude')

            self.orbital_speed = self.conn.add_stream(getattr, self.vessel.orbit, 'speed')
            self.apoapsis = self.conn.add_stream(getattr, self.vessel.orbit, 'apoapsis_altitude')
            self.periapsis = self.conn.add_stream(getattr, self.vessel.orbit, 'periapsis_altitude')
            self.orbital_period = self.conn.add_stream(getattr, self.vessel.orbit, 'period')
            self.time_to_apoapsis = self.conn.add_stream(getattr, self.vessel.orbit, 'time_to_apoapsis')
            self.time_to_periapsis = self.conn.add_stream(getattr, self.vessel.orbit, 'time_to_periapsis')
            self.inclination = self.conn.add_stream(getattr, self.vessel.orbit, 'inclination')
            self.eccentricity = self.conn.add_stream(getattr, self.vessel.orbit, 'eccentricity')
            self.long_asc_node = self.conn.add_stream(getattr, self.vessel.orbit, 'longitude_of_ascending_node')
            self.ecc_anomaly = self.conn.add_stream(getattr, self.vessel.orbit, "eccentric_anomaly")

            self.mass = self.conn.add_stream(getattr, self.vessel, 'mass')
            self.thrust = self.conn.add_stream(getattr, self.vessel, 'thrust')
            self.max_thrust = self.conn.add_stream(getattr, self.vessel, 'max_thrust')
            self.surface_gravity = self.conn.add_stream(getattr, self.vessel.orbit.body, 'surface_gravity')

            self.res_names = list(set([res.name for res in self.vessel.resources.all]))
            self.res_streams = []
            for res in self.res_names:
                self.res_streams.append(self.conn.add_stream(self.vessel.resources.amount, res))

            self.resIDS_names = list(set([res.name for res in self.vessel.resources_in_decouple_stage(self.vessel.control.current_stage, False).all]))
            self.resIDS_streams = []
            for res in self.resIDS_names:
                self.resIDS_streams.append(self.conn.add_stream(self.vessel.resources_in_decouple_stage(self.vessel.control.current_stage, False).amount, res))

            self.mean_altitude = self.conn.add_stream(getattr, self.vessel.flight(orbital_ref_frame), "mean_altitude")
            self.latitude = self.conn.add_stream(getattr, self.vessel.flight(orbital_ref_frame), "latitude")
            self.longitude = self.conn.add_stream(getattr, self.vessel.flight(orbital_ref_frame), "longitude")
            self.arg_periapsis = self.conn.add_stream(getattr, self.vessel.orbit, "argument_of_periapsis")

    def update_streams(self):
        for res in self.resIDS_streams:
            res.remove()

        self.resIDS_names = list(set([res.name for res in self.vessel.resources_in_decouple_stage(self.vessel.control.current_stage, False).all]))
        self.resIDS_streams = []
        for res in self.resIDS_names:
            self.resIDS_streams.append(self.conn.add_stream(self.vessel.resources_in_decouple_stage(self.vessel.control.current_stage, False).amount, res))

    def update(self, data_array, msgQ):
        # Manage notebook tab switching
        if self.panel_connected:
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

        self.notebook_page = self.notebook.index(self.notebook.select())

        # Update reused elements
        OI_data = [si_val(self.orbital_speed()) + 'm/s',
                      si_val(self.apoapsis(), 2) + 'm',
                      si_val(self.periapsis(), 2) + 'm',
                      sec2time(self.orbital_period()),
                      sec2time(self.time_to_apoapsis()),
                      sec2time(self.time_to_periapsis()),
                      '{0:.2f} deg'.format(degrees(self.inclination())),
                      '{0:.4f}'.format(self.eccentricity()),
                      '{0:.2f} deg'.format(degrees(self.long_asc_node()))]


        SI_data = [si_val(self.agl_altitude(), 3) + 'm',
                      '{0:.1f} deg'.format(self.pitch()),
                      '{0:.0f} deg'.format(self.heading()),
                      '{0:.1f} deg'.format(self.roll()),
                      si_val(self.speed(), 2) + 'm/s',
                      si_val(self.v_speed(), 2) + 'm/s',
                      si_val(self.h_speed(), 2) + 'm/s']

        try:
            twr = self.max_thrust() / (self.mass() * self.surface_gravity())
        except ZeroDivisionError:
            twr = 0

        VI_data = [si_val(self.mass() * 1000) + 'g',
                      si_val(self.max_thrust(), 3) + 'N',
                      si_val(self.thrust(), 3) + 'N',
                      '{0:.2f}'.format(twr)]

        # Tab 9 - Maintanance
        if self.notebook_page == 8:
            temp = ['{0:08b}'.format(data_array[0]),
                    '{:d}ms'.format(data_array[27]),
                    '{0:.0f}deg'.format(data_array[18] * 0.69310345 - 68.0241379),
                    '{0:.0f}%'.format(data_array[28] / 255 * 100),
                    '{0:.0f}%'.format(data_array[19] / 255 * 100)]

            self.T9_SD.update(temp)

            # Tab 9 --> Left Frame --> Digital Data SubframeLabel
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
                    '{0:08b}'.format(data_array[33]),
                    '{0:08b}'.format(data_array[34]),
                    '{0:08b}'.format(data_array[35]),
                    '{0:08b}'.format(data_array[36]),
                    '{0:08b}'.format(data_array[37]),
                    '{0:08b}'.format(data_array[38])
                    ]
            self.T9_DI.update(temp)

            # Tab 9 --> Left Frame --> Analog Data SubframeLabel
            temp = [data_array[20],
                    data_array[21],
                    data_array[22],
                    data_array[23],
                    data_array[24],
                    data_array[25],
                    data_array[26]]
            self.T9_AI.update(temp)
            # Tab 9 --> Left Frame --> Analogure Data SubframeLabel
            # temp = ["ON" if is_set(data_array[29], 0) else "OFF",
                    # "RUNNING" if is_set(data_array[29], 1) else "INITIATING",
                    # "CONNECTED" if is_set(data_array[29], 2) else "DISCON",
                    # data_array[30],
                    # bytes2int([data_array[33], data_array[34]]),
                    # "CONNECTED" if is_set(data_array[29], 3) else "DISCON",
                    # data_array[31],
                    # bytes2int([data_array[35], data_array[36]]),
                    # "CONNECTED" if is_set(data_array[29], 4) else "DISCON",
                    # data_array[32],
                    # bytes2int([data_array[37], data_array[38]])]
            #self.T9_AP.update(temp)

        # Update message area
        if not msgQ.empty():
            m = msgQ.get()
            self.msgL1.set(self.msgL2.get())
            self.msgL2.set(self.msgL3.get())
            self.msgL3.set(self.msgL4.get())
            self.msgL4.set(msg_prefix[m[0]] + ': ' + m[1])

    def connect_panel(self, data_array, msgQ):
        # Start the panel controller module
        self.panel_proc = Process(target=panel_control, args=(data_array, msgQ))
        self.panel_proc.start()
        self.panel_connected = True
        self.panel_status.set("Connected")
        self.styles.configure('Ind.TLabel', background='green')

    def disconnect_panel(self):
        self.panel_proc.terminate()
        self.panel_connected = False
        self.panel_status.set("Disconnected")
        self.styles.configure('Ind.TLabel', background='light grey')

    def exit(self,root):
        if self.panel_connected:
            self.disconnect_panel()
        root.destroy()
        quit()