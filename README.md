# NeuroBytes CLI

## Installation
Install dependencies
>sudo apt-get install gdb-arm-none-eabi python-pip

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
>neurobytes program -e {FILE_NAME.elf}

## NID
Network Interface Device