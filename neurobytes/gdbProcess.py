import threading
import time
import re
import subprocess
import click
from neurobytes.exceptions import ConnectError

class gdbProcess(object):

    gdb_command = "arm-none-eabi-gdb"
    gdb_batch_option = "--batch"

    connected = False

    def __init__(self, interval, interface):

        self.interval = interval
        self.interface = interface
        self.gdb_command_option = "--command=" + self.interface.file
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while (True):
            try:
                gdbProc = subprocess.Popen([self.gdb_command, self.gdb_batch_option, self.gdb_command_option],stdout=subprocess.PIPE, universal_newlines=True)
                while(True):
                    for line in iter(gdbProc.stdout.readline, ""):
                        
                        if line == "":
                            break
                        if "can't attach" in line:
                            self.connected = False
                        elif "attached" in line:
                            if self.connected == False:
                                click.echo("Attached")
                            self.connected = True
                        click.echo('loop')
                        click.echo(line)
                        
                    print 'loop'
                    if gdbProc.stdout.readline() == "" or gdbProc.poll is None:
                        break
                    time.sleep(0.01)
            except ConnectError:
                click.echo("No device attached")
                time.sleep(0.1)
                pass
            except:
                click.echo("error")
                print "Failed to start GDB server"
            time.sleep(self.interval)