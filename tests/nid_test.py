#!/bin/python2.7

import struct

def read_data(address, length):
    inferior = gdb.selected_inferior()
    mem = inferior.read_memory(address, length*4)
    data = struct.unpack_from('i'*length, mem)
    return data

gdb.execute("tar ext /dev/ttyACM1")

gdb.execute("mon s")

gdb.execute("attach 1")

for data in read_data(0x08000300, 1):
    print data

gdb.execute("detach")
gdb.execute("quit")


