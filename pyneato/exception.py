class MyNeatoLoginException(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

class MyNeatoRobotException(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

class MyNeatoException(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message

class MyNeatoUnsupportedDevice(Exception):
    def __init__(self, message):
        Exception.__init__(self)
        self.message = message
