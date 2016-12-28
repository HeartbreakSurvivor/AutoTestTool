#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys,binascii
import importlib
importlib.reload(sys)

from mainboard import Ui_UsartTool
#from Serial import MySerial
from PyQt4 import QtCore, QtGui
from serial import Serial
import serial.tools.list_ports

#from Keyevent import Keyevent
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
        self.textEdit.setReadOnly(True)
        self.DatabitsComboBox.setCurrentIndex(3)#default 8 bits
        self.BaudRataComboBox.setCurrentIndex(1)#default 9600

        #serial configuration
        self._serial = Serial()
        self.GetSerialPorts()
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

        self.installEventFilter(self)
        self.isopen = 0

        #用定时器每个一定时间去扫描有没数据收到，只要在打开串口才开始即使
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.Receive)

    #actions
    def GetSerialPorts(self):
        port_list = list(serial.tools.list_ports.comports())
        if len(port_list) <= 0:
            print("Can't find serial port")
        else:
            print(port_list.__len__())
            for x in port_list:
                print(x.device)
                self.SerialNumComboBox.addItem(x.device)

    def Switchserial(self):
        #clickstatus = self.pushButton.isChecked() #串口开关状态检查
        if not self.isopen: #如果串口为关闭状态
            #获得串口参数
            #comread = int(self.label_3.   text())-1 #端口号，计算机端口都是从0开始算的，所以减去1
            #baudrate = self._serial.baudrate
            port = self.SerialNumComboBox.currentText()
            baudrate = int(self.BaudRataComboBox.currentText()) #波特率
            bytesize = int(self.DatabitsComboBox.currentText())
            stopbits = int(self.StopBitsComboBox.currentText())
            parity = self.ParityComboBox.currentText()
            try:
                #self._serial = Serial(port="COM1", baudrate=9600,bytesize=8,stopbits=1)
                print(port)
                self._serial.port = port
                self._serial.baudrate = baudrate
                self._serial.bytesize = bytesize
                self._serial.stopbits = stopbits
                self._serial.parity = parity
                self._serial.open()
                self.isopen = 1
            except:
                QtGui.QMessageBox.information(self, "Tips", "串口打开失败，请确认串口号是否被占用")
                return False
            self.timer.start(30)  # 30ms刷新一次界面
            print("open the serial and timer start")
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
            self.timer.stop()
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

    def Receive(self):
        if self.isopen:
            try:
                bytesToRead = self._serial.inWaiting()
            except:
                bytesToRead = 0
                self.Switchserial()
                print("error ")
            if bytesToRead > 0:
                self.recstr = self._serial.read(bytesToRead)
                #self.textEdit.append(self.recstr.decode(encoding='utf-8'))
                self.textEdit.append(self.recstr.decode(encoding='gbk'))
                #self.textEdit.append((str)(hexshow(self.recstr)))
                if self.textEdit.toPlainText().__len__() > 10000:
                    bytesToRead = 0
                    self.textEdit.clear()
            else:
                pass
        else:
            pass

    def close(self):
        if self.serial.isOpen():
            self.serial.close()

    def run(self):
        while 1:
            data = self.Receive()
            if not data:
                break
            self.qtobj.emit(SIGNAL("NewData"), data)

        self.serial.close()

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
        self._serial.write("ic#".encode())
    def MenuKey(self):
        self._serial.write("is#".encode())
    def MinusKey(self):
        self._serial.write("ir$".encode())
    def PlusKey(self):
        self._serial.write("it\"".encode())

    def eventFilter(self, watched, event):
        #if watched == self.ExitButton or watched == self.MenuButton or watched == self.PlusButton or watched == self.MinusButton:
        if event.type() == QtCore.QEvent.KeyPress:
            keyEvent = QtGui.QKeyEvent(event)
            if self._serial.isOpen():
                if keyEvent.key() == QtCore.Qt.Key_W:
                    self._serial.write("ic#".encode())
                    print("the W key pressed")
                elif keyEvent.key() == QtCore.Qt.Key_S:
                    self._serial.write("is#".encode())
                    print("the S key pressed")
                elif keyEvent.key() == QtCore.Qt.Key_A:
                    self._serial.write("ir$".encode())
                    print("the A key pressed")
                elif keyEvent.key() == QtCore.Qt.Key_D:
                    self._serial.write("it\"".encode())
                    print("the D key pressed")
            else:
                QtGui.QMessageBox.information(self, "Tips", "请先打开串口")

        if event.type() == QtCore.QEvent.KeyRelease:
            pass
            #print("the up key released")
        return QtGui.QWidget.eventFilter(self, watched, event)

    def event(self, QEvent):
        if QEvent.type() == QtCore.QEvent.KeyPress:
            if QEvent.key() == QtCore.Qt.Key_Tab:
                print(" tab key")
                return True
            if QEvent.key() == QtCore.Qt.Key_Up:
                print(" up key")
                return True
            if QEvent.key() == QtCore.Qt.Key_Down:
                print("down key")
                return True
        return QtGui.QWidget.event(self,QEvent)

    def keyPressEvent(self, event):
        if event.modifiers() == QtCore.Qt.ControlModifier:
            if event.key() == QtCore.Qt.Key_Home:
                print("the I key")
            elif event.key() == QtCore.Qt.Key_Down:
                print("the down key")
            elif event.key() == QtCore.Qt.Key_Left:
                print("the left key")
            elif event.key() == QtCore.Qt.Key_Right:
                print("the right key")
            elif event.key() == QtCore.Qt.Key_Home:
                print("the home key")
            else:
               print("what the fuck!")

if __name__ == "__main__":
    print(__name__)
    print(__author__)
    print(__version__)
    app = QtGui.QApplication(sys.argv)
    #app.installEventFilter(app)
    #ui = Ui_UsartTool()

    ui = MainWidget()
    ui.show()
    #ui.setupUi(UsartTool)
    sys.exit(app.exec_())
