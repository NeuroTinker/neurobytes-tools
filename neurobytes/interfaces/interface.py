import re

class interface(object):

    def __init__(self):
        self.file = str(__file__)
        self.file = re.sub(r'pyc', 'py', self.file)
        print self.file