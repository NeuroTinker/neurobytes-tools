# NeuroBytes CLI

## Installation
Install dependencies
>sudo apt-get install gdb-arm-none-eabi python-pip python-tk

Install neurobytes CLI,
>sudo pip install neurobytes

## Updating
Update with pip
>sudo pip install neurobytes --upgrade

## Flashing NeuroBytes
Update stored firmware,
>neurobytes update

Flash latest firmware
>neurobytes flash

Flash *.elf file from your current directory (file name optional)
>neurobytes flash -e {FILE_NAME.elf}

## NID
Communicate with a NeuroBytes network using the Network Interface Device (NID).

Start the NID command shell,
>neurobytes nid

The NID shell establishes communication with a NID device and then waits for commands.

NID shell is indicated with,
>(nid) [type command]

Currently supported NID commands:
>Send a blink command
>>(nid) blink
>
>Identify device to monitor on channel number [channel] and issue unique commands to. [channel] defaults to 1
>>(nid) identify [channel]