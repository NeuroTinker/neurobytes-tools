#!/bin/python2.7

def read_data(address, length):
    inferior = gdb.selected_inferior()
    mem = inferior.read_memory(adddress, length)
    data = struct.unpack_from('i'*length, mem)
    return data

gdb.execute("tar ext /dev/ttyACM0")

gdb.execute("mon s")

gdb.execute("attach 1")

print read_data(0x08000300, 1)

gdb.execute("detach")
gdb.execute("quit")


