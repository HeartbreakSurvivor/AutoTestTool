#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys,binascii
from mainboard import Ui_UsartTool
#from Serial import MySerial
from PyQt4 import QtCore, QtGui
from serial import Serial

__author__ = "bigzhanghao"
__version__ = "0.1"

class MainWidget(QtGui.QWidget,Ui_UsartTool):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.setupUi(self)  # 显示主窗口
        self.DatabitsComboBox.setCurrentIndex(3)#default 8 bits
        self.BaudRataComboBox.setCurrentIndex(1)#default 9600
        #serial configuration
        self._serial = Serial()

        #Setup the singal
        self.SwitchButton.connect(self.SwitchButton, QtCore.SIGNAL('clicked()'), self.Switchserial)
        self.SendDataButton.connect(self.SendDataButton, QtCore.SIGNAL('clicked()'), self.Send)
        self.ClearDataButton.connect(self.ClearDataButton, QtCore.SIGNAL('clicked()'), self.Clear)
        self.HexDisCheckbox.connect(self.HexDisCheckbox,QtCore.SIGNAL('clicked()'),self.DisHex)
        self.HexSendcheckBox.connect(self.HexSendcheckBox, QtCore.SIGNAL('clicked()'), self.SendHex)
        self.isopen = 0
    #actions
    def Switchserial(self):
        #clickstatus = self.pushButton.isChecked() #串口开关状态检查
        if not self.isopen: #如果串口为关闭状态
            #获得串口参数
            #comread = int(self.label_3.   text())-1 #端口号，计算机端口都是从0开始算的，所以减去1
            baudrate = self._serial.baudrate
            baudrate = int(self.BaudRataComboBox.currentText()) #波特率
            bytesize = int(self.DatabitsComboBox.currentText())
            stopbits = int(self.StopBitsComboBox.currentText())
            parity = self.ParityComboBox.currentText()
            try:
                #self._serial = Serial(port="COM1", baudrate=9600,bytesize=8,stopbits=1)
                self._serial.port = "COM1"
                self._serial.baudrate = baudrate
                self._serial.bytesize = bytesize
                self._serial.stopbits = stopbits
                self._serial.parity = parity
                self._serial.open()
                self.isopen = 1
            except:
                print("open serial fail!")
                return False
            print(self._serial.isOpen())
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
            self.SerialNumComboBox.setEnabled(True)
            self.DatabitsComboBox.setEnabled(True)
            self.BaudRataComboBox.setEnabled(True)
            self.StopBitsComboBox.setEnabled(True)
            self.ParityComboBox.setEnabled(True)
            self.SwitchButton.setText("打开串口")

    def Send(self):
        if not self.isopen:
            QtGui.QMessageBox.information(self,"Tips","请先打开串口")
            return
        else:
            try:
                if not self.HexSendcheckBox.isChecked():
                    self._serial.write(self.DataToSend.text().encode())
                else:
                    print("erro121311r")
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

    def DisHex(self):
        if self.HexSendcheckBox.isChecked():
            print("Dis Hex checked")
        else:
            print("Dis Hex no checked")

    def SendHex(self):
        print(self.DataToSend.text())
        if self.HexSendcheckBox.isChecked():
            print("Send Hex checked")
        else:
            print("Send Hex no checked")

if __name__ == "__main__":
    print(__name__)
    print(__author__)
    print(__version__)
    app = QtGui.QApplication(sys.argv)

    #ui = Ui_UsartTool()
    ui = MainWidget()
    ui.show()
    #ui.setupUi(UsartTool)
    sys.exit(app.exec_())
