import urllib
import re
import click
import struct

class firmware(object):
    git_base = "https://github.com/NeuroTinker/NeuroBytes_"
    git_extension = "/FIRMWARE/bin/main.elf?raw=true"

    git_device_names = [
        "Interneuron",
        "Photoreceptor",
        "Motor_Neuron",
        "Touch_Sensor",
        "Tonic_Neuron",
        "Force_Sensor"
    ]

    git_branches = [
        "master",
        "development"
    ]

    fingerprint_elf_address = 0x23e00

    def edit_fingerprint(self, fin, unique_id):
        fstream = open(fin, 'r+')
        fstream.seek(self.fingerprint_elf_address + 0x8)
        fstream.write(struct.pack('i', unique_id))
        fstream.close()

    def git_to_elf_translator(self, git_name, branch):
        elf_name = self.file
        elf_name += git_name.lower()
        elf_name += ("_dev" if branch=="development" else "")
        elf_name += ".elf"
        return elf_name

    def make_url(self, device, branch):
        return self.git_base + device + "/blob/" + branch + self.git_extension

    def __init__(self, elf_file=re.sub(r'elfs.pyc', '', __file__)):
        self.file = str(elf_file)
        print self.file

    def update(self):
        with click.progressbar(self.git_device_names, label="updating stored firmware") as bar:
            for branch in self.git_branches:
                for name in bar:
                    urllib.urlretrieve(self.make_url(name, branch), self.git_to_elf_translator(name, branch))