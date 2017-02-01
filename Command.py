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
        print("this is Minus command")

class PlusCommand(command):
    def exec(self):
        print("this is Plus Command")

class PowerCommand(command):
    def exec(self):
        print("this is Power command")

