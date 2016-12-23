#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys,binascii
from mainboard import Ui_UsartTool
#from Serial import MySerial
from PyQt4 import QtCore, QtGui
from serial import Serial
from Keyevent import Keyevent
__author__ = "bigzhanghao"
__version__ = "0.1"

def hexshow(argv):
    result = ''
    hLen = len(argv)
    for i in range(hLen):
        hvol = ord(argv[i])
        hhex = '%02x'%hvol
        result += hhex + ' '
        print("hexshow: ", result)
    return result


class MainWidget(QtGui.QWidget,Ui_UsartTool):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.setupUi(self)  # 显示主窗口
        #self.textEdit.setReadOnly(True)
        self.DatabitsComboBox.setCurrentIndex(3)#default 8 bits
        self.BaudRataComboBox.setCurrentIndex(1)#default 9600
        #serial configuration
        self._serial = Serial()
        self._keyevent = Keyevent()
        #Setup the singal
        self.SwitchButton.connect(self.SwitchButton, QtCore.SIGNAL('clicked()'), self.Switchserial)
        self.SendDataButton.connect(self.SendDataButton, QtCore.SIGNAL('clicked()'), self.Send)
        self.ClearDataButton.connect(self.ClearDataButton, QtCore.SIGNAL('clicked()'), self.Clear)
        self.HexDisCheckbox.connect(self.HexDisCheckbox,QtCore.SIGNAL('clicked()'),self.DisHex)
        self.HexSendcheckBox.connect(self.HexSendcheckBox, QtCore.SIGNAL('clicked()'), self.SendHex)

        self.ExitButton.connect(self.ExitButton, QtCore.SIGNAL('clicked()'), self.ExitKey)
        self.MenuButton.connect(self.MenuButton, QtCore.SIGNAL('clicked()'), self.MenuKey)
        self.MinusButton.connect(self.MinusButton,QtCore.SIGNAL('clicked()'),self.MinusKey)
        self.PlusButton.connect(self.PlusButton, QtCore.SIGNAL('clicked()'), self.PlusKey)
        #event filter

        self.ExitButton.installEventFilter(self)
        # self.MenuButton.installEventFilter(self)
        # self.PlusButton.installEventFilter(self)
        # self.MinusButton.installEventFilter(self)
        # self.FactoryButton.installEventFilter(self)
        # self.SourceButton.installEventFilter(self)
        # self.PowerButton.installEventFilter(self)

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
                    #hexer = list(self.DataToSend.text())
                    self._serial.write(self.DataToSend.text().encode())
                else:
                    self._serial.write(self.DataToSend.text().encode())
            except:
                print("send data fail")
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
        if self.HexDisCheckbox.isChecked():#check
            temphex = hexshow(self.textEdit.toPlainText())
            self.textEdit.clear()
            self.textEdit.setText(temphex)
        else:#cancel check
            print("Dis Hex no checked")

    def SendHex(self):
        self.DataToSend.clear()
        if self.HexSendcheckBox.isChecked():#check
            print("Send Hex checked")
        else:# cancel check
            print("Send Hex no checked")

    def ExitKey(self):
        print("sdasdas")
        try:
            self._serial.write("ic#".encode())
        except:
            print("send data fail")
    def MenuKey(self):
        self._serial.write("\x69,\x73,\x23".encode())
    def MinusKey(self):
        self._serial.write("\x69,\x72,\x24".encode())
    def PlusKey(self):
        self._serial.write("\x69,\x74,\x22".encode())

    def eventFilter(self, watched, event):
        if watched == self.ExitButton or watched == self.MenuButton or watched == self.PlusButton or watched == self.MinusButton:
            if event.type() == QtCore.QEvent.KeyPress:
                keyEvent = QtGui.QKeyEvent(event)
                if keyEvent.key() == QtCore.Qt.Key_Up:
                    self._serial.write("ic#".encode())
                if keyEvent.key() == QtCore.Qt.Key_Down:
                    self._serial.write("ic#".encode())
                    print("the down key pressed")
                if keyEvent.key() == QtCore.Qt.Key_Left:
                    self._serial.write("ic#".encode())
                    print("the up key pressed")
                if keyEvent.key() == QtCore.Qt.Key_Right:
                    self._serial.write("ic#".encode())
                    print("the down key pressed")
            if event.type() == QtCore.QEvent.KeyRelease:
                print("the up key released")
        return QtGui.QWidget.eventFilter(self, watched, event)

    # def keyPressEvent(self, event):
    #     #if event.modifiers() == QtCore.Qt.ControlModifier:
    #     if event.key() == QtCore.Qt.Key_Up:
    #         print("the up key")
    #     elif event.key() == QtCore.Qt.Key_Down:
    #         print("the down key")
    #     elif event.key() == QtCore.Qt.Key_Left:
    #         print("the left key")
    #     elif event.key() == QtCore.Qt.Key_Right:
    #         print("the right key")
    #     elif event.key() == QtCore.Qt.Key_Home:
    #         print("the home key")
    #     #else:
    #     #    print("what the fuck!")

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
