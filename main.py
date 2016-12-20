#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys,binascii
from mainboard import Ui_UsartTool
#from Serial import MySerial
from PyQt4 import QtCore, QtGui
from serial import Serial

__author__ = "bigzhanghao"
__version__ = "0.1"

class MainWidget(Ui_UsartTool):
    def __init__(self,parent=None):
        super(Ui_UsartTool, self).__init__()
        self.setupUi(UsartTool)  # 显示主窗口

        #serial configuration
        #self._serial = Serial()

        #Setup the singal
        self.SwitchButton.connect(self.SwitchButton, QtCore.SIGNAL('clicked()'), self.Switchserial)
        self.SendDataButton.connect(self.SendDataButton, QtCore.SIGNAL('clicked()'), self.Send)
        self.ClearDataButton.connect(self.ClearDataButton, QtCore.SIGNAL('clicked()'), self.Clear)
        self.isopen = 0
    #actions
    def Switchserial(self):
        #clickstatus = self.pushButton.isChecked() #串口开关状态检查
        if not self.isopen: #如果串口为关闭状态
            #print("open the serial")

            #获得串口参数
            #comread = int(self.label_3.   text())-1 #端口号，计算机端口都是从0开始算的，所以减去1

            bandrate = int(self.BaudRataComboBox.currentIndex()) #波特率
            #databit = SERIAL_DATABIT_ARRAY[self.shujuwei.currentIndex()] #数据位
            #stopbit = SERIAL_STOPBIT_ARRAY[self.jiaoyanwei.currentIndex()] #校验位
            #checkbit = SERIAL_CHECKBIT_ARRAY[self.tingzhiwei.currentIndex()] #停止位
            print(bandrate)

            try:
                #self._serial = Serial(port="COM1", baudrate=9600,bytesize=8,parity=0,stopbits=1,timeout=0)
                self._serial = Serial(port="COM1", baudrate=9600,bytesize=8,stopbits=1)
                self.isopen = 1
            except:
                print("open serial fail!")
                return False

            self.SerialNumComboBox.setEnabled(False)
            self.DatabitsComboBox.setEnabled(False)
            self.BaudRataComboBox.setEnabled(False)
            self.StopBitsComboBox.setEnabled(False)
            self.ParityComboBox.setEnabled(False)
            self.SwitchButton.setText("关闭串口")
            #打开串口
        else:   #关闭串口、使能各个窗口
            #self._serial.close()
            #self.timer.stop()
            try:
                self._serial.close()
                self.isopen = 0
            except:
                print("close the serial fail")
            print("close the serial")
            self.SerialNumComboBox.setEnabled(True)
            self.DatabitsComboBox.setEnabled(True)
            self.BaudRataComboBox.setEnabled(True)
            self.StopBitsComboBox.setEnabled(True)
            self.ParityComboBox.setEnabled(True)
            self.SwitchButton.setText("打开串口")

    def Send(self):
        if not self.isopen:
            print("请先打开串口")
            #QtGui.QMessageBox.information(self, "Tips", u"请先打开串口")
            return
        else:
            self.textEdit.setText("send data")
            self._string = "hello python\n"
            self.a = 'a'
            #self.hex_ = binascii.b2a_hex(self.a.encode())

            try:
                #self._serial.write(self._string.encode())
                self._serial.write(self.a.encode())
            except:
                self.DataToSend.setText("send fail")
                return
        """self.ui.onSendData(data, _type)
        if _type == "hex":
            data = Util.toHex(''.join(data.split()))
        self.serial.send(data, _type)
        """

    def Clear(self):
        print("clear the window")
        self.textEdit.clear()
        self.DataToSend.clear()
        return

if __name__ == "__main__":
    print(__name__)
    print(__author__)
    print(__version__)
    app = QtGui.QApplication(sys.argv)
    UsartTool = QtGui.QDialog()
    #ui = Ui_UsartTool()
    ui = MainWidget(UsartTool)
    #ui.setupUi(UsartTool)
    UsartTool.show()
    sys.exit(app.exec_())
