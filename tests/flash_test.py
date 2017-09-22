#from neurobytes import gdbProcess
#from neurobytes.interfaces import *

import subprocess
import time

command = "arm-none-eabi-gdb"
batch = "--batch"
script = "--command=/usr/local/lib/python2.7/dist-packages/neurobytes/interfaces/blackmagic.py"
try:
    gdbProc = subprocess.Popen([command, batch, script], stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
except:
    print 'error'
while (True):
    time.sleep(0.1)
    print gdbProc.stdout.readlines()
#bmp = blackmagic.blackmagic()
#gdb = gdbProcess.gdbProcess(0.1, bmp)