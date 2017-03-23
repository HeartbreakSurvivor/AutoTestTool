from abc import ABCMeta,abstractmethod

class command(object):
    def __init__(self,serial):
        self._serial = serial #the receiver

    __metaclass__ = ABCMeta
    @abstractmethod
    def execute(self):
        pass

class MinusCommand(command):
    def execute(self):
        self._serial.send("ir$".encode())

class PlusCommand(command):
    def execute(self):
        self._serial.send("it\"".encode())

class PowerCommand(command):
    def execute(self):
        print("this is Power command")

class MeunCommand(command):
    def execute(self):
        self._serial.send("is#".encode())

class ExitCommand(command):
    def execute(self):
        self._serial.send("ic#".encode())

class EcoCommand(command):
    def execute(self):
        print("this is Eco command")

class FactoryCommand(command):
    def execute(self):
        print("this is factory command")

class SourceCommand(command):
    def execute(self):
        self._serial.send("iu".encode())
        print("this is Source command")