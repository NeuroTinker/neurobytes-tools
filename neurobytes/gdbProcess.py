import threading
import time
import re
import subprocess
import click
import os
from neurobytes.exceptions import ConnectError

class gdbProcess(object):

    gdb_command = "arm-none-eabi-gdb"
    gdb_batch_option = "--batch"
    gdb_file_option = None

    connected = False

    def __init__(self, interval, interface, local_elf=None):

        self.interval = interval
        self.interface = interface
        self.gdb_command_option = "--command=" + self.interface.file
        self.gdb_file_option = local_elf
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True
        thread.start()

    def run(self):
        while (True):
            flash_count = 0
            try:
                if self.gdb_file_option is not None:
                    gdbProc = subprocess.Popen([self.gdb_command, self.gdb_batch_option, self.gdb_command_option, self.gdb_file_option],stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
                else:
                    gdbProc = subprocess.Popen([self.gdb_command, self.gdb_batch_option, self.gdb_command_option],stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, universal_newlines=True)
                while(True):
                    for line in iter(gdbProc.stdout.readline, ""):
                        #click.echo(line)
                        if line == "":
                            break
                        elif "can't attach" in line:
                            self.connected = False
                        elif "attached" in line:
                            if self.connected == False:
                                pass
                            self.connected = True
                        elif "oad" in line:
                            flash_count += 1
                            if flash_count == 1:
                                bar = click.progressbar(length=4, label="flashing...")
                                bar.update(1)
                            elif flash_count <4:
                                bar.update(1)
                            else:
                                flash_count = 0
                                time.sleep(0.1)
                                bar.update(1)
                                click.echo(" COMPLETE")
                        elif "Connected " in line:
                            click.echo(line)
                        elif "debug" in line:
                            click.echo(line)
                            click.echo('debug')
                        else:
                            pass
                            #click.echo(line)
                        
                    if gdbProc.stdout.readline() == "" or gdbProc.poll is None:
                        break
                    time.sleep(0.01)
                gdbProc.kill()
            except ConnectError:
                click.echo("No device attached")
                time.sleep(0.1)
                pass
            except:
                click.echo("error")
                print "Failed to start GDB server"
            time.sleep(self.interval)