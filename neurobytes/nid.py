import serial
import matplotlib.pyplot as plt
import numpy as np
import time
import click
import threading
import struct

ping_message = [
    chr(0b11100000),
    chr(0b00000000),
    chr(0b00000000),
    chr(0b00000000)
]

identify_message = lambda chan: [
    chr(0b11000000),
    chr(0b01000000 | (chan<<3)),
    chr(0b00000000),
    chr(0b00000000)
]

blink_message = [
    chr(0b10010000),
    chr(0b00000000),
    chr(0b00000000),
    chr(0b00000000)
]

version_message = lambda dev, ver: [
    chr(0b11000000),
    chr(0b10000000 | (dev<<1) | (ver>>7)),
    chr(ver<<1),
    chr(0b00000000)
]

FIRE_THRESHOLD = 10000

# NID_SELECTED_COMMAND
# 0b1101 - selected command header
# 3-bit channel
# 5-bit parameter
# 16-bit data
parameter_message = lambda chan, param, val: [
    chr(0b11010000 | (chan<<1)),
    chr((param<<4) | (val>>12)),
    chr(0xFF & val>>4),
    chr(0xFF & val<<4)
]

class potentialGraph(object):

    channel_data = {
        1 : None,
        2 : None,
        3 : None,
        4 : None
    }

    subplots = {
        1 : None,
        2 : None,
        3 : None,
        4 : None
    }

    class channelSubplot(object):
        plot_pos_lookup = {
            1 : 221,
            2 : 222,
            3 : 223,
            4 : 224
        }

        def __init__(self, channel, fig):
            self.pos = self.plot_pos_lookup[channel]
            self.fig = fig
            self.ax = self.fig.add_subplot(self.pos)
            self.x = np.arange(100)
            self.y = [0] * 100
            self.y[0] = -15000
            self.y[1] = 15000

            self.li, = self.ax.plot(self.x,self.y)

            self.ax.relim()
            self.ax.autoscale_view(True, True, True)
        
        def update(self, data):
            self.y[:-1] = self.y[1:]
            self.y[-1:] = [data]
            self.ax.autoscale_view(True, True, True)
            self.li.set_ydata(self.y)

    # realtime potential graph
    def __init__(self):
        self.fig = plt.figure()
        self.fig.canvas.draw()
        plt.show(block=False)

    def update(self, data, channel):
        if self.subplots[channel] is not None:
            self.subplots[channel].update(data)
        self.fig.canvas.draw()

    def add_channel(self, channel):
        if self.subplots[channel] is None:
            self.subplots[channel] = self.channelSubplot(channel, self.fig)
        self.fig.canvas.draw()

class nidHandler(object):
    
    def io_loop_runnable(self):
        # run loop to get commands from user
        while True:
            raw = raw_input('(nid) ').split()
            cmd = raw[0]
            args = raw[1:]
            self.command_lookup[cmd](self, args)
            self._cmd_ev.wait() 

    def nid_ping_timed(self):
        # timed loop to send NID pings
        #self._cmd_msg = ping_message
        self._ping_ev.clear()
        self.nid_thread = threading.Timer(0.2, self.nid_ping_timed)
        self.nid_thread.start()

    def serial_loop_runnable(self):
        # run loop to send/receive serial messages
        while True:
            # check for message from NID
            # read if a whole packet (4 bytes) has been received
            count = self.usb.in_waiting
            num_msg_waiting = count / 4
            if num_msg_waiting >= 1 and count%4 == 0:
                for i in xrange(num_msg_waiting):
                    raw_msg = self.usb.read(4)
                    msg_as_uint32 = struct.unpack_from(">I", raw_msg)
                    header = (msg_as_uint32[0] >> 28) & 0b1111
                    try:
                        handler = self.message_lookup[header]
                        handler(self, raw_msg)
                    except:
                        pass
            elif not self._ping_ev.isSet():
                self.write_message(ping_message)
                self._ping_ev.set()
            elif not self._cmd_ev.isSet():
                self.write_message(self._cmd_msg)
                self._cmd_ev.set()

    def send_blink(self, *args):
        self._cmd_ev.clear()
        self._cmd_msg = blink_message
        click.echo('Blink sent')
    
    def send_version(self, *args):
        # There should be two arguments: device and version
        device = args[0]
        version = args[1]
        self._cmd_ev.clear()
        self._cmd_msg = version_message(device, version)
        click.echo('Version check sent')
    
    def set_parameter(self, *args):
        # One argument: "set [channel]". Ask what parameter they want to set.
        channel = args[0]
        click.echo("Adjusting parameter on channel " + str(channel))
        raw1 = raw_input("Parameter to set: ")
        if raw1 not in self.parameter_lookup:
            click.echo('Parameter not found.')
        else:
            raw2 = raw_input("Enter new value: ")
            self._cmd_ev.clear()
            self._cmd_msg = parameter_message(int(channel[0]), self.parameter_lookup[raw1], int(raw2))
            click.echo("Parameter set.")


    def send_identify(self, *args):
        try:
            channel = int(args[0][0])
        except:
            channel = 1
        if channel == []:
            channel = 1  
        print channel      
        self._cmd_ev.clear()
        self._cmd_msg = identify_message(channel)

    def recv_quit(self, *args, **kwargs):
        self._quit_ev.set()

    def recv_data(self, raw_msg):
        msg_segments = struct.unpack_from(">Hh", raw_msg)
        header = msg_segments[0]
        data = msg_segments[1]
        channel = (header >> 5) & 0b111
        if self.graph_controller.subplots[channel] is not None:
            if data > FIRE_THRESHOLD:
                self._data_fire = True
            self._data_val = data
            self._data_ch = channel
            self._data_ev.set()
            #self.graph_controller.update(data, channel) 
        else:
            click.echo ("Channel " + str(channel) + " identified")
            self.graph_controller.add_channel(channel)
            # TODO: send an identify cmd message after opening new channel
    
    parameter_lookup = {
        'dendrite 1' : 0b010,
        'dendrite 2' : 0b011,
        'dendrite 3' : 0b100,
        'dendrite 4' : 0b101,
        'pwm_span' : 0b101,
        'pwm_zero' : 0b111,
        'delay' : 0b111
    }

    command_lookup = {
        'identify' : send_identify,
        'blink' : send_blink,
        'quit'  : recv_quit,
        'version' : send_version,
        'set' : set_parameter,
        'save' : save_data
    }

    ch_freq = {
        1 : 0,
        2 : 0,
        3 : 0,
        4 : 0
    }

    ch_period = {
        1 : 0,
        2 : 0,
        3 : 0,
        4 : 0
    }

    message_lookup = {
        0b1010 : recv_data
    }

    def __init__(self, serial_port='/dev/ttyACM1'):
        # initialize serial connection with NID
        self.usb = serial.Serial(serial_port, baudrate=38400)

        # start communication threads
        self._cmd_msg = None
        self._cmd_ev = threading.Event()
        self._ping_ev = threading.Event()
        self._quit_ev = threading.Event()
        self._data_ev = threading.Event()
        self._data_val = 0

        self.io_thread = threading.Thread(target=self.io_loop_runnable)
        self.nid_thread = threading.Timer(0.2, self.nid_ping_timed)
        self.serial_thread = threading.Thread(target=self.serial_loop_runnable)

        self.io_thread.daemon = True
        self.nid_thread.daemon = True
        self.serial_thread.daemon = True
    
    def start(self):
        # start graphing window
        self.graph_controller = potentialGraph()
        self.graph_controller.add_channel(1)
        self.graph_controller.add_channel(2)
        self.graph_controller.add_channel(3)
        self.graph_controller.add_channel(4)
        self._data_ch = 1
        self._data_val = 0

        self.io_thread.start()
        self.nid_thread.start()
        self.serial_thread.start()

    def wait_for_quit(self):
        while not self._quit_ev.isSet():
            if self._data_ev.isSet():
                if self._data_fire:
                    # channel had a firing event. Increment frequency counter
                    self.graph_controller.update(self.ch_period, 1)
                self.graph_controller.update(self._data_val, self._data_ch)
                self._data_ev.clear()
            time.sleep(0.01)
            if self.ch_period[0] < 100:
                self.ch_period[0] += 1
        self._quit_ev.wait()
        quit()

    def write_message(self, message):
        if message is not None:
            for byte in message:
                self.usb.write(byte)