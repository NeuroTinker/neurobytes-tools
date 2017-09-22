class Error(Exception):
    pass

class ConnectError(Error):
    
    def __init__(self, message):
        self.message = message

class InterfaceError(Error):

    def __init__(self, message):
        self.message = message