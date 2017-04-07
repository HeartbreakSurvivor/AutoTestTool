from abc import ABCMeta,abstractmethod

class command(object):
    def __init__(self,serial):
        self._serial = serial #the receiver
    __metaclass__ = ABCMeta
    @abstractmethod
    def execute(self,keymsg):
        pass

class MinusCommand(command):
    def execute(self,keymsg):
        if keymsg.isCustomize:
            self._serial.send(keymsg.getContent().encode())
        else:
            self._serial.send("ir$".encode())

class PlusCommand(command):
    def execute(self,keymsg):
        if keymsg.isCustomize:
            self._serial.send(keymsg.getContent().encode())
        else:
            self._serial.send("it\"".encode())

class PowerCommand(command):
    def execute(self, keymsg):
        if keymsg.isCustomize:
            self._serial.send(keymsg.getContent().encode())
        else:
            self._serial.send("iv ".encode())

class MeunCommand(command):
    def execute(self, keymsg):
        if keymsg.isCustomize:
            self._serial.send(keymsg.getContent().encode())
        else:
            self._serial.send("is#".encode())

class ExitCommand(command):
    def execute(self,keymsg):
        if keymsg.isCustomize:
            self._serial.send(keymsg.getContent().encode())
        else:
            self._serial.send("iq%".encode())

class FactoryCommand(command):
    def execute(self,keymsg):
        if keymsg.isCustomize:
            self._serial.send(keymsg.getContent().encode())
        else:
            self._serial.send("id2".encode())

class SourceCommand(command):
    def execute(self,keymsg):
        if keymsg.isCustomize:
            self._serial.send(keymsg.getContent().encode())
        else:
            self._serial.send("iu!".encode())