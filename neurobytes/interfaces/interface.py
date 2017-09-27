import re

class interface(object):

    local_elf = None

    def __init__(self):
        self.file = str(__file__)
        self.file = re.sub(r'pyc', 'py', self.file)
        self.firmware_dir = re.sub(r'interface.py', '', self.file)
        print self.file