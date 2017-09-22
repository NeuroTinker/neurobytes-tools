import os
import re
import struct
import neurobytes.exceptions
import time

device_types = {
    1 : "interneuron",
    2 : "photoreceptor",
    3 : "motor_neuron",
    4 : "tonic_neuron",
    5 : "touch_sensor",
    6 : "vestibular",
    7 : "force_sensor",
    8 : "cochlea"
}

fingerprint_elf_address = 0x023e00
elf_path = "/usr/local/lib/python2.7/dist-packages/neurobytes/firmware/"

def read_fingerprint():
    inferior = gdb.selected_inferior()
    mem = inferior.read_memory(0x08003e00, 12) # this seems wrong. shouldnt it be 0x08023e00?
    fingerprint = struct.unpack_from('iii', mem)
    return fingerprint

def make_elf(device_type, unique_id):
    firmware_path = elf_path+device_types[device_type]+".elf"
    with open(firmware_path, 'r+') as f:
        f.seek(fingerprint_elf_address + 0x8)
        f.write(struct.pack('i', unique_id))
        f.close()
    return firmware_path

if __name__ == "__main__":
    print 'gdb alive'
    # gdb script

    try:
        gdb.execute("tar extended-remote /dev/ttyACM0")
    except:
        try:
            gdb.execute("tar extended-remote /dev/ttyACM1")
        except:
            try:
                gdb.execute("tar extended-remote /dev/ttyACM2")
            except:
                raise neurobytes.exceptions.InterfaceError("BlackMagic Probe not detected.")

    try:
        gdb.execute("mon tpwr enable")
        str = gdb.execute("mon swdp_scan")
    except:
        pass

    try:
        gdb.execute("attach 1")
        print "attached"
    except:
        print "can't attach"
        pass
    try:
        (device_type, firmware_version, unique_id) = read_fingerprint() 
        firmware_path = make_elf(device_type, unique_id)
        gdb.execute("file " + firmware_path)
        gdb.execute("load")
    except:
        pass
    
    #gdb.execute('run')
    
    gdb.execute("quit")


class blackmagic(object):

    def __init__(self):
        self.file = str(__file__)
        self.file = re.sub(r'pyc', 'py', self.file)