from neurobytes import gdbProcess
from neurobytes.interfaces import blackmagic
from neurobytes.firmware import firmware
from neurobytes import nid as nidO
import click
import time
from neurobytes.exceptions import ConnectError
from shutil import copyfile

@click.group()
def cli():
    pass
@click.command()

def nid():
    click.echo('Initializing Network Interface Device...')
    try:
        nid_handle = nidO.nidHandler()
    except:
        click.echo("Couldn't connect to NID! Make sure the NID is connected and try again")
    nid_handle.start()
    nid_handle.wait_for_quit()

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
    if interface == 'blackmagic':
        interface_obj = blackmagic.blackmagic()
    elif interface == 'raspi':
        pass
        # TODO: add bit-banged raspi swd interfac.e probably split interfaces into gdb and openocd

    try:
        if elf:
            click.echo("Flashing with " + elf)
            gdb_thread = gdbProcess.gdbProcess(0.01, interface_obj, elf)
        else:
            gdb_thread = gdbProcess.gdbProcess(0.01, interface_obj)
    except ConnectError:
        print "connect error"
    while True:
        time.sleep(1)

cli.add_command(flash)
cli.add_command(update)
cli.add_command(nid)
