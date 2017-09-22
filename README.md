#NeuroBytes CLI

##Installation
If you don't have pip and python,
>sudo apt-get install python-pip

Install neurobytes CLI,
>sudo pip install neurobytes

##Flashing NeuroBytes
Update stored firmware,
>neurobytes update

Flash latest firmware
>neurobytes program

Flash *.elf file from your current directory (file name optional)
>neurobytes program -e {FILE_NAME.elf}