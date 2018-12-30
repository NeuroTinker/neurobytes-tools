import os
import re
import struct
import neurobytes.exceptions
import time
import csv
import datetime

# TODO: move the gdb script to a gdb interface file

device_types = {
    0 : "virgin",
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
import csv
import os
import pwd
import datetime
import time
elf_path = "/usr/local/lib/python2.7/dist-packages/neurobytes/firmware/"
log_path = os.path.expanduser('~') + "/neurobytes_log.csv"

def get_new_fingerprint():
    with open(log_path, 'r+') as f:
        reader = csv.DictReader(f, delimiter=',', quotechar='|')
        for row in reader:
            pass
        new_fingerprint=int(row['id'])+1
    return new_fingerprint
        
def log_fingerprint(unique_id, device_type, version):
    ts = time.time()
    timestamp = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S')
    # user = os.getLogin()
    user = pwd.getpwuid(os.getuid())[0]
    with open(log_path, 'a') as f:
        writer = csv.writer(f, delimiter=',', quotechar='|')
        # writer.writerow('id': unique_id, 'version': version, 'type': device_type, 'user': user, 'timestamp': timestamp)
        writer.writerow([unique_id, timestamp, version, device_type, user])


def read_fingerprint():
    inferior = gdb.selected_inferior()
    mem = inferior.read_memory(0x08003e00, 12)
    fingerprint = struct.unpack_from('iii', mem)
    return fingerprint

def release_elf(device_type):
    firmware_path = elf_path+device_types[device_type]+".elf"
    return firmware_path

def make_elf(file_path, unique_id):
    with open(file_path, 'r+') as f:
        f.seek(fingerprint_elf_address + 0x8)
        f.write(struct.pack('i', unique_id))
        f.close()

def local_elf():
    # return the local elf file path, if it exists.
    try:
        f_status = gdb.execute('info files', to_string=True)
        f_status = f_status.split("\n")
        print f_status
        if f_status:
            for line in f_status:
                if 'Symbols from' in line:
                    line = line.replace("Symbols from ", "")
                    return line.strip("\t'\".")
        return None
    except:
        return None

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
        gdb.execute("mon enter_swd")
    except:
        pass

    try:
        gdb.execute("mon tpwr enable")
        str = gdb.execute("mon swdp_scan")
    except:
        pass

    try:
        gdb.execute("mon enter_swd")
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
        if device_type == 0:
            unique_id = get_new_fingerprint()
        print "Connected to {} {}\n".format(device_types[device_type], unique_id)
        print device_types[device_type]
        firmware_path = local_elf()
        if firmware_path is None:
            firmware_path = release_elf(device_type)
        print firmware_path
        make_elf(firmware_path, unique_id)
        gdb.execute("file " + firmware_path)
        gdb.execute("load")
    except:
        pass
    
    try:
        gdb.execute('run')
    except:
        pass
    
    gdb.execute("quit")


class blackmagic(object):

    def __init__(self):
        self.file = str(__file__)
        self.file = re.sub(r'pyc', 'py', self.file)
        self.firmware_dir = re.sub(r'interface.py', '', self.file)