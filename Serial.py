import threading

from serial import Serial


class MySerial(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.terminate = False

    def open(self,settings):
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
