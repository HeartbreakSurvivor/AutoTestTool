from serial import Serial
import serial.tools.list_ports

class MySerial(object):
    def __init__(self):
        self.serial = Serial()

    #actions
    def GetSerialPorts(self):
        port_list = list(serial.tools.list_ports.comports())#local variable
        return port_list

    def open(self,settings):
        self.serial.open()

    def close(self):
        self.serial.close()

    def send(self,data):
        self.serial.write(data)

