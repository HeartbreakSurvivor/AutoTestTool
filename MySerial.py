from serial import Serial
import serial.tools.list_ports

class MySerial(Serial):
    def __init__(self):
        super(MySerial,self).__init__()
        #self.serial = Serial()

    #actions
    def GetSerialPorts(self):
        port_list = list(serial.tools.list_ports.comports())#local variable
        return port_list

    def send(self,data):
        """the child class call the methond delcare in the father class """
        #Serial.write(self,data)  #1
        super(MySerial,self).write(data)  #2

