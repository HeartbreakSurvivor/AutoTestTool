import threading

from serial import Serial
from time import sleep
from mainboard import Ui_UsartTool

class MySerial(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.terminate = False

    def open(self,settings):
        self.serial.port = Ui_UsartTool.co
        try:
            self.serial = Serial(settings["Port"],)
            self.serial.flushInput()
            self.serial.flushOutput()
        except Exception as e:
            return False

        return True,"success"

    def close(self):
        if self.serial.is_open():
            self.close()

    def send(self,data,_type):
        self.serial.write(data)

    @property
    def receive(self):
        data, quit = None, False
        while 1:
            data = self.serial.read(1)
            if data == '':
                continue
            while 1:
                n = self.serial.inWaiting()
                if n > 0:
                    data = "%s%s" % (data, self.serial.read(n))
                    sleep(0.02) # data is this interval will be merged
                else:
                    quit = True
                    break
            if quit:
                break
        return data

