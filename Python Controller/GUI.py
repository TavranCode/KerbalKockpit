from tkinter import *
from tkinter import ttk
import krpc
from multiprocessing import Process
from math import degrees

from Utilities import is_set, si_val, sec2time, SubframeLabel, SubframeVar, norm
from Settings import *
from PanelControl import panel_control


class Application:
    def __init__(self, root, data_array, msgQ):

        # Define Styles
        self.styles = ttk.Style()
        self.styles.configure('Display.TLabel', font=('helvetica', '18'), padding=(10, 0), background='black', foreground='blue')
        self.styles.configure('Msg.TLabel', font=('helvetica', '10'), padding=(10, 0), background='black', foreground='blue')
        self.styles.configure('Ind.TLabel', font=('helvetica', '16', 'bold'), padding=(10, 0), relief='raised', anchor='center')
        self.styles.configure('TNotebook.Tab', font=('helvetica', '14', 'bold'), padding=(10, 0))
        self.styles.configure('TLabelframe.Label', font=('helvetica', '24', 'bold'), background='black')
        self.styles.configure('TLabelframe', background='black')
        self.styles.configure('TFrame', relief='ridge', background='black')
        self.styles.configure('TButton', font=('helvetica', '16', 'bold'))
        self.styles.configure('Ind.TLabel', font=('helvetica', '16', 'bold'), padding=(10, 0), relief='raised', anchor='center')

        # Create the notebook and define its tabs
        self.notebook = ttk.Notebook(root, width=c_screen_size_x - 2, height=c_notebook_size_y)

        tab1 = ttk.Frame(self.notebook, borderwidth=10)
        tab2 = ttk.Frame(self.notebook, borderwidth=10)
        tab3 = ttk.Frame(self.notebook, borderwidth=10)
        tab4 = ttk.Frame(self.notebook, borderwidth=10)
        tab5 = ttk.Frame(self.notebook, borderwidth=10)
        tab6 = ttk.Frame(self.notebook, borderwidth=10)
        tab7 = ttk.Frame(self.notebook, borderwidth=10)
        tab8 = ttk.Frame(self.notebook, borderwidth=10)
        tab9 = ttk.Frame(self.notebook, borderwidth=10)

        self.notebook.add(tab1, text='Launch')
        self.notebook.add(tab2, text='Orbital')
        self.notebook.add(tab3, text='Landing')
        self.notebook.add(tab4, text='Rondezvous')
        self.notebook.add(tab5, text='Flight')
        self.notebook.add(tab6, text='Runway')
        self.notebook.add(tab7, text='Rover')
        self.notebook.add(tab8, text='Systems')
        self.notebook.add(tab9, text='Maintenance')

        # Tab 1 - Orbital
        self.T1L_OI = SubframeLabel(tab1, 'Orbit Info', ('Orbital Speed:', 'Apoapsis:', 'Periapsis:', 'Orbital Period:',
                                                         'Time to Apoapsis:', 'Time to Periapsis:', 'Inclination:', 'Ecentricity:',
                                                         'LAN:'), 440, 320)
        self.T1L_OI.grid(row=0, column=0)

        self.T1L_SI = SubframeLabel(tab1, 'Surface Info', ('Altitude (AGL):', 'Pitch:', 'Heading:', 'Roll:',
                                                           'Speed:', 'Vertical Speed:', 'Horizontal Speed:'), 440, 280)
        self.T1L_SI.grid(row=1, column=0)

        self.T1L_VI = SubframeLabel(tab1, 'Vessel Info', ('Vessel Mass:', 'Max Thrust:', 'Current Thrust:', 'Surface TWR:'), 440, 160)
        self.T1L_VI.grid(row=0, column=1)

        # Tab 2 - Orbital
        self.T2L_OI = SubframeLabel(tab2, 'Orbit Info', ('Orbital Speed:', 'Apoapsis:', 'Periapsis:', 'Orbital Period:',
                                                         'Time to Apoapsis:', 'Time to Periapsis:', 'Inclination:', 'Ecentricity:',
                                                         'LAN:'), 420, 320)
        self.T2L_OI.grid(row=0, column=0)

        self.T2L_VI = SubframeLabel(tab2, 'Vessel Info', ('Vessel Mass:', 'Max Thrust:', 'Current Thrust:', 'Surface TWR:'), 420, 160)
        self.T2L_VI.grid(row=1, column=0)

        # Tab 3 - Landing
        self.T3L_OI = SubframeLabel(tab3, 'Orbit Info', ('Orbital Speed:', 'Apoapsis:', 'Periapsis:', 'Orbital Period:',
                                                         'Time to Apoapsis:', 'Time to Periapsis:', 'Inclination:', 'Ecentricity:',
                                                         'LAN:'), 440, 320)
        self.T3L_OI.grid(row=0, column=0)

        self.T3L_SI = SubframeLabel(tab3, 'Surface Info', ('Altitude (AGL):', 'Pitch:', 'Heading:', 'Roll:',
                                                           'Speed:', 'Vertical Speed:', 'Horizontal Speed:'), 440, 280)
        self.T3L_SI.grid(row=1, column=0)

        self.T3L_VI = SubframeLabel(tab3, 'Vessel Info', ('Vessel Mass:', 'Max Thrust:', 'Current Thrust:', 'Surface TWR:'), 440, 160)
        self.T3L_VI.grid(row=0, column=1)

        # Tab 4 - Rondezvous
        self.T4L_OI = SubframeLabel(tab4, 'Orbit Info', ('Orbital Speed:', 'Apoapsis:', 'Periapsis:', 'Orbital Period:',
                                                         'Time to Apoapsis:', 'Time to Periapsis:', 'Inclination:', 'Ecentricity:',
                                                         'LAN:'), 440, 320)
        self.T4L_OI.grid(row=0, column=0)

        self.T4L_SI = SubframeLabel(tab4, 'Surface Info', ('Altitude (AGL):', 'Pitch:', 'Heading:', 'Roll:',
                                                           'Speed:', 'Vertical Speed:', 'Horizontal Speed:'), 440, 280)
        self.T4L_SI.grid(row=1, column=0)

        self.T4L_TI = SubframeLabel(tab4, 'Target Info', ('Target:', 'Closest Approach:', 'Intercept Time:', 'Intercept Speed:',
                                                          'Dist to Target:', 'Target Velocity',
                                                          'Rel. Distance x:', 'Rel. Distance y:', 'Rel. Distance z:',
                                                          'Rel. Velocity x:', 'Rel. Velocity y:', 'Rel. Velocity z:'), 440, 440)
        self.T4L_TI.grid(row=0, column=1)

        self.T4L_VI = SubframeLabel(tab4, 'Vessel Info', ('Vessel Mass:', 'Max Thrust:', 'Current Thrust:', 'Surface TWR:'), 440, 160)
        self.T4L_VI.grid(row=1, column=1)

        # Tab 8 - Systems
        self.T8L_VD = SubframeVar(tab8, 'Resource Data', 10, 420, 400)
        self.T8L_VD.grid(row=0, column=0)

        # Tab 9 - Maintenance
        # Tab 9 --> Left Frame - Arduino Data
        self.T9L = ttk.LabelFrame(tab9, text='Arduino Data', width=700, height=600)

        # Tab 9 --> Left Frame --> Sub Frames
        self.T9L_SD = SubframeLabel(self.T9L, 'Status Data', ('Status Byte:', 'Frame Time:', 'Temperature:', 'Fan Speed:', 'Dimmer:'), 320, 200)
        self.T9L_SD.grid(row=0, column=0)

        self.T9L_DI = SubframeLabel(self.T9L, 'Digital Inputs', ('Pins 8-10:', 'Pins 22-29:', 'Pins 30-37:', 'Pins 38-45:', 'Pins 46-53:', 'MUX 0 Bank A:',
                                                                 'MUX 0 Bank B:', 'MUX 1 Bank A:', 'MUX 1 Bank B:', 'MUX 2 Bank B:', 'MUX 3 Bank B:',
                                                                 'MUX 4 Bank B:'), 320, 520)
        self.T9L_DI.grid(row=0, column=1, rowspan=2)

        self.T9L_AI = SubframeLabel(self.T9L, 'Analogue Inputs', ('Rotation X:', 'Rotation Y:', 'Rotation Z:', 'Translation X:', 'Translation Y:',
                                                                  'Translation Z:', 'Throttle:'), 320, 300)
        self.T9L_AI.grid(row=1, column=0)

        self.T9L.grid()

        # Grid in the notebook once all content is done
        self.notebook.grid(column=0, row=0)

        # Build the lower area for the messages and buttons
        lowerframe = ttk.Frame(root, width=c_screen_size_x - 2, height=135)

        # Build the Message box with four data lines
        self.msgframe = ttk.LabelFrame(lowerframe, text='Status Messages', width=850, height=120)

        self.msgL1 = StringVar()
        self.msgL2 = StringVar()
        self.msgL3 = StringVar()
        self.msgL4 = StringVar()

        self.msg1 = ttk.Label(self.msgframe, style='Msg.TLabel', textvariable=self.msgL1).grid(row=0, sticky=(E, W))
        self.msg2 = ttk.Label(self.msgframe, style='Msg.TLabel', textvariable=self.msgL2).grid(row=1, sticky=(E, W))
        self.msg3 = ttk.Label(self.msgframe, style='Msg.TLabel', textvariable=self.msgL3).grid(row=2, sticky=(E, W))
        self.msg4 = ttk.Label(self.msgframe, style='Msg.TLabel', textvariable=self.msgL4).grid(row=3, sticky=(E, W))

        self.msgframe.grid(sticky=E, padx=5, pady=5, rowspan=2)
        self.msgframe.grid_propagate(False)

        # Buttons
        self.panel_status = StringVar()
        self.panel_status.set("Disconnected")

        ttk.Button(lowerframe, text='Connect Panel', command=lambda: self.connect_panel(data_array, msgQ), width=15).grid(column=1, row=0, sticky=SE, padx=5, pady=5)
        ttk.Button(lowerframe, text='Disconnect Panel', command=self.disconnect_panel, width=15).grid(column=1, row=1, sticky=NE, padx=5, pady=5)
        self.panel_status_button = ttk.Label(lowerframe, textvariable=self.panel_status, width=13, style='Ind.TLabel', relief='raised').grid(column=2, row=0, sticky=(S, E, W), padx=5, pady=8)
        ttk.Button(lowerframe, text='Exit', command=root.destroy, width=15).grid(column=2, row=1, sticky=NE, padx=5, pady=5)

        # Once the lower area is complete, grid it in
        lowerframe.grid(row=1, sticky=(E, W), padx=5)
        lowerframe.grid_propagate(False)

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
        self.mass = None
        self.thrust = None
        self.max_thrust = None
        self.surface_gravity = None
        self.res_names = None
        self.res_streams = None

        # initialise attributes that require a state
        self.panel_connected = False
        self.game_connected = False
        self.vessel_connected = False

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

        self.speed = self.conn.add_stream(getattr, self.vessel.flight(self.vessel.orbit.body.reference_frame), 'speed')
        self.h_speed = self.conn.add_stream(getattr, self.vessel.flight(self.vessel.orbit.body.reference_frame), 'horizontal_speed')
        self.v_speed = self.conn.add_stream(getattr, self.vessel.flight(self.vessel.orbit.body.reference_frame), 'vertical_speed')
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

        self.mass = self.conn.add_stream(getattr, self.vessel, 'mass')
        self.thrust = self.conn.add_stream(getattr, self.vessel, 'thrust')
        self.max_thrust = self.conn.add_stream(getattr, self.vessel, 'max_thrust')
        self.surface_gravity = self.conn.add_stream(getattr, self.vessel.orbit.body, 'surface_gravity')

        self.res_names = list(set([res.name for res in self.vessel.resources.all]))
        self.res_streams = []
        for res in self.res_names:
            self.res_streams.append(self.conn.add_stream(self.vessel.resources.amount, res))

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

        # Tab 1 - Launch
        T1L_OI_data = [si_val(self.orbital_speed()) + 'm/s',
                       si_val(self.apoapsis()) + 'm',
                       si_val(self.periapsis()) + 'm',
                       sec2time(self.orbital_period()),
                       sec2time(self.time_to_apoapsis()),
                       sec2time(self.time_to_periapsis()),
                       '{0:.2f} deg'.format(degrees(self.inclination())),
                       '{0:.4f}'.format(self.eccentricity()),
                       '{0:.2f} deg'.format(degrees(self.long_asc_node()))]
        self.T1L_OI.update(T1L_OI_data)

        T1L_SI_data = [si_val(self.agl_altitude(), 3) + 'm',
                       '{0:.1f} deg'.format(self.pitch()),
                       '{0:.0f} deg'.format(self.heading()),
                       '{0:.1f} deg'.format(self.roll()),
                       si_val(self.speed(), 2) + 'm/s',
                       si_val(self.v_speed(), 2) + 'm/s',
                       si_val(self.h_speed(), 2) + 'm/s']
        self.T1L_SI.update(T1L_SI_data)

        try:
            twr = self.max_thrust() / (self.mass() * self.surface_gravity())
        except ZeroDivisionError:
            twr = 0

        T1L_VI_data = [si_val(self.mass() * 1000) + 'g',
                       si_val(self.max_thrust(), 0) + 'N',
                       si_val(self.thrust(), 0) + 'N',
                       '{0:.2f}'.format(twr)]
        self.T1L_VI.update(T1L_VI_data)

        # Tab 3 - Landing
        self.T3L_OI.update(T1L_OI_data)

        self.T3L_VI.update(T1L_VI_data)

        self.T3L_SI.update(T1L_SI_data)
        
        # Tab 4 - Rondezvous
        self.T4L_OI.update(T1L_OI_data)

        self.T4L_VI.update(T1L_VI_data)

        self.T4L_SI.update(T1L_SI_data)

        target_vessel = self.conn.space_center.target_vessel

        if target_vessel is None:
            T4L_TI_data = ["No Target",
                           '',
                           '',
                           '',
                           '',
                           '',
                           '',
                           '',
                           '',
                           '',
                           '',
                           '']
        else:
            target_pos = target_vessel.position(self.vessel.reference_frame)
            target_vel = target_vessel.velocity(self.vessel.reference_frame)
            T4L_TI_data = [target_vessel.name,
                           '',
                           '',
                           '',
                           si_val(norm(target_pos),1)+'m',
                           si_val(norm(target_vel),1)+'m/s',
                           '{0:.2f}m'.format(target_pos[0]),
                           '{0:.2f}m'.format(target_pos[1]),
                           '{0:.2f}m'.format(target_pos[2]),
                           '{0:.2f}m/s'.format(target_vel[0]),
                           '{0:.2f}m/s'.format(target_vel[1]),
                           '{0:.2f}m/s'.format(target_vel[2])]

        self.T4L_TI.update(T4L_TI_data)

        # Tab 8 = Systems
        # Tab 8 --> Left Frame
        # Tab 8 --> Left Frame --> Resource Data
        res_vals = []
        for res in self.res_streams:
            res_vals.append('{0:.0f}'.format(res()))
        self.T8L_VD.update(self.res_names, res_vals)

        # Tab 9 - Maintanance
        # Tab 9 --> Left Frame
        # Tab 9 --> Left Frame --> Status Data SubframeLabel
        temp = ['{0:08b}'.format(data_array[0]),
                '{:d}ms'.format(data_array[23]),
                '{0:.0f}deg'.format(data_array[14] * 0.69310345 - 68.0241379),
                '{0:.0f}%'.format(data_array[24] / 255 * 100),
                '{0:.0f}%'.format(data_array[15] / 255 * 100)]

        self.T9L_SD.update(temp)

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
                '{0:08b}'.format(data_array[11]),
                '{0:08b}'.format(data_array[12])]
        self.T9L_DI.update(temp)

        # Tab 9 --> Left Frame --> Analogure Data SubframeLabel
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
