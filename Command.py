from abc import ABCMeta,abstractmethod

class command(object):
    def __init__(self,serial):
        self._serial = serial #the receiver

    __metaclass__ = ABCMeta
    @abstractmethod
    def exec(self):
        pass

class MinusCommand(command):
    def exec(self):
        self._serial.send("this is Minus command")
        print("this is Minus command")

class PlusCommand(command):
    def exec(self):
        self._serial.send("this is Plus command")
        print("this is Plus Command")

class PowerCommand(command):
    def exec(self):
        print("this is Power command")

class MeunCommand(command):
    def exec(self):
        print("this is Menu command")

class ExitCommand(command):
    def exec(self):
        print("this is Exit Command")

class FactoryCommand(command):
    def exec(self):
        print("this is factory command")

class SourceCommand(command):
    def exec(self):
        print("this is Source command")