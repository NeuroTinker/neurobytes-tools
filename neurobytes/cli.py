from neurobytes import gdbProcess
from neurobytes.interfaces import blackmagic
from neurobytes.firmware import firmware
import click
import time
from neurobytes.exceptions import ConnectError

@click.group()
def cli():
    pass

@click.command()

def update():
    elf_controller = firmware.firmware()
    elf_controller.update()

@click.command()

# specify elf file option
@click.option(
    '--elf',
    '-e',
    help="Specify a firmware (*.elf) file to flash"
    # default *.elf in current directory
)

# use dev branch option
@click.option(
    '--dev',
    '-d',
    is_flag=True,
    help="Use development firmware version (from git development branch)"
)

# specify programming interface option
@click.option(
    '--interface',
    '-i',
    default="blackmagic",
    help="Specify programming interface to use"
)
def flash(elf, dev, interface):
    try:
        gdb_thread = gdbProcess.gdbProcess(0.01, blackmagic.blackmagic())
    except ConnectError:
        print "connect error"
    while True:
        time.sleep(1)

cli.add_command(flash)
cli.add_command(update)