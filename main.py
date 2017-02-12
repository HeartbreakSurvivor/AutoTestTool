#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys,binascii
import importlib
importlib.reload(sys)

from keyedit import Ui_KeyEdit
from MainWindow import Ui_MainWindow
from PyQt4 import QtCore, QtGui
from serial import Serial
import serial.tools.list_ports

from MySerial import MySerial
from Command import *

from KeyMsg import KeyMsg
import keyedit


#from Keyevent import Keyevent
__author__ = "bigzhanghao"
__version__ = "0.1"

global Keymsg_1 , Keymsg_2 , Keymsg_3 , Keymsg_4 , Keymsg_5 , Keymsg_6 , Keymsg_7
Keymsg_1 = KeyMsg()
Keymsg_2 = KeyMsg()
Keymsg_3 = KeyMsg()
Keymsg_4 = KeyMsg()
Keymsg_5 = KeyMsg()
Keymsg_6 = KeyMsg()
Keymsg_7 = KeyMsg()

KeyMessage = [Keymsg_1, Keymsg_2, Keymsg_3, Keymsg_4, Keymsg_5, Keymsg_6, Keymsg_7]

def hexshow(argv):
    result = ''
    hLen = len(argv)
    for i in range(hLen):
        hvol = ord(argv[i])
        hhex = '%02x'%hvol
        result += hhex + ' '
        #print("hexshow: ", result)
    return result

class KeyEdit(QtGui.QWidget,Ui_KeyEdit):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.__KeyName = list[self.KeyName1,self.KeyName2,self.KeyName3,self.KeyName4,
                              self.KeyName5,self.KeyName6,self.KeyName7]
        self.__Customize = list[self.KeyCustome1,self.KeyCustome2,self.KeyCustome3,self.KeyCustome4,
                                self.KeyCustome5,self.KeyCustome6,self.KeyCustome7]
        self.__Content = list[self.SendMsg1,self.SendMsg2,self.SendMsg3,self.SendMsg4,self.SendMsg5,
                              self.SendMsg6,self.SendMsg7]
        self.__VirtualKey = list[self.VirtualKey1,self.VirtualKey2,self.VirtualKey3,self.VirtualKey4,
                                self.VirtualKey5,self.VirtualKey6,self.VirtualKey7]

        self.KeyCustome1.connect(self.KeyCustome1, QtCore.SIGNAL('clicked()'), self.IsCustomized)
        self.KeyCustome2.connect(self.KeyCustome2, QtCore.SIGNAL('clicked()'), self.IsCustomized)
        self.KeyCustome3.connect(self.KeyCustome3, QtCore.SIGNAL('clicked()'), self.IsCustomized)
        self.KeyCustome4.connect(self.KeyCustome4, QtCore.SIGNAL('clicked()'), self.IsCustomized)
        self.KeyCustome5.connect(self.KeyCustome5, QtCore.SIGNAL('clicked()'), self.IsCustomized)
        self.KeyCustome6.connect(self.KeyCustome6, QtCore.SIGNAL('clicked()'), self.IsCustomized)
        self.KeyCustome7.connect(self.KeyCustome7, QtCore.SIGNAL('clicked()'), self.IsCustomized)

    def IsCustomized(self):
        for i in range(0,self.__Customize.__len__()):
            if self.__Customize[i].isChecked():
                KeyMessage[i].isCustomize = 1
                self.__Content[i].setReadOnly(True)
            else:
                KeyMessage[i].isCustomize = 0
                self.__Content[i].setReadOnly(False)

    def GetEntityKey(self):
        for i in range(0,self.__VirtualKey.__len__()):
            if self.__VirtualKey.count(self.__VirtualKey[i].CurrentText()) > 1:
                QtGui.QMessageBox.information(self, "Tips", "定义了相同的按键")
                break
            if self.__VirtualKey[i].CurrentText() is not None:
                KeyMessage.setEntityKey(self.__VirtualKey[i].CurrentText())

    def GetSendMsg(self):
        TempMsg = ""
        for i in range(0,self.__Content.__len__()):
            if self.__Customize[i].isChecked():
                TempMsg = self.__Content[i].text()
                KeyMessage[i].setContent(TempMsg)

    def GetKeyName(self):
        for i in range(0,self.__KeyName.__len__()):
            #if self.__KeyName[i].Length() >= 10:
            #    print("what's time")
            KeyMessage[i].setName(self.__KeyName[i].text())

class MainWidget(QtGui.QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)

        self.__CommandList = []

        self.setupUi(self)

        self.textEdit.setReadOnly(True)
        self.action8.checked = 1
        self.action9600.checked = 1

        #self.menu.setCuhrrentIndex(3)#default 8 bits
        #self.BaudRataComboBox.setCurrentIndex(1)#default 9600
        """
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
        self.PowerButton.connect(self.MenuButton, QtCore.SIGNAL('clicked()'), self.PowerKey)
        self.SourceButton.connect(self.MinusButton,QtCore.SIGNAL('clicked()'),self.SourceKey)
        self.FactoryButton.connect(self.PlusButton, QtCore.SIGNAL('clicked()'), self.FactoryKey)
        #event filter
        """
        #serial configuration
        #self._serial = Serial()
        self._serial = MySerial()
        self.GetSerialPorts()

        #Command pattern
        #Create the commands
        self.__MenuCmd = MeunCommand(self._serial)
        self.__ExitCmd = ExitCommand(self._serial)
        self.__PowerCmd = PowerCommand(self._serial)
        self.__PlusCmd = PlusCommand(self._serial)
        self.__MinusCmd = MinusCommand(self._serial)
        self.__EcoCmd = EcoCommand(self._serial)
        self.__SourceCmd = SourceCommand(self._serial)
        self.__FactoryCmd = FactoryCommand(self._serial)

        self.SetCommands(self.__MenuCmd)
        self.SetCommands(self.__MinusCmd)
        self.SetCommands(self.__ExitCmd)
        self.SetCommands(self.__PowerCmd)
        self.SetCommands(self.__PlusCmd)
        self.SetCommands(self.__EcoCmd)
        self.SetCommands(self.__SourceCmd)
        self.SetCommands(self.__FactoryCmd)


        Keymsg_1.setName("Exit")
        Keymsg_2.setName("Minus")
        Keymsg_3.setName("Plus")
        Keymsg_4.setName("Menu")
        Keymsg_5.setName("Power")
        Keymsg_6.setName("Source")
        Keymsg_7.setName("Factory")



        self.installEventFilter(self)
        self.isopen = 0

        #用定时器每个一定时间去扫描有没数据收到，只要在打开串口才开始即使
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.Receive)

        self._str = ""
        #private variable

    #add new command to the command list
    def SetCommands(self,Command):
        self.__CommandList.append(Command)

    #invoker execute the command
    def Execute(self,Command):
        if Command in self.__CommandList:
            Idx = self.__CommandList.index(Command)
            print(Idx)
            #Command.execute(self)
            self.__CommandList[Idx].execute()


    #actions
    def GetSerialPorts(self):
        port_list = self._serial.GetSerialPorts()
        if len(port_list):
            for x in port_list:
                pass
                #self.SerialNumComboBox.addItem(x.device)
        else:
            print("Can't find serial port")
            pass

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
        else:
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
                    self._serial.send(self.DataToSend.text().encode())
                else:
                    self._serial.send(self.DataToSend.text().encode())
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
                self._str +=(self.recstr.decode(encoding='gbk'))

                #self.textEdit.append(self.recstr.decode(encoding='gbk'))
                #self.textEdit.insertPlainText(self.recstr.decode(encoding='gbk'))

                #self._str = self.textEdit.toPlainText()

                #if self.textEdit.toPlainText().__len__() > 10000:
                if self._str.__len__() > 10000:
                    bytesToRead = 0
                    self._str = ""
                    self.textEdit.clear()

                if self.HexDisCheckbox.isChecked():
                    temphex = hexshow(self._str)
                    self.textEdit.setText(temphex)
                else:
                    self.textEdit.setText(self._str)
            else:
                pass
        else:
            pass

    def close(self):
        if self.serial.isOpen():
            self.serial.close()

    def Clear(self):
        self._str = ""
        self.textEdit.clear()
        self.DataToSend.clear()
        return

    def DisHex(self):
        if self.HexDisCheckbox.isChecked():#check
            temphex = hexshow(self._str)
            self.textEdit.clear()
            self.textEdit.setText(temphex)
        else:#cancel check
            self.textEdit.clear()
            self.textEdit.setText(self._str)

    def SendHex(self):
        self.DataToSend.clear()
        if self.HexSendcheckBox.isChecked():#check
            print("Send Hex checked")
        else:# cancel check
            print("Send Hex no checked")

    def ExitKey(self):
        self.Execute(self.__ExitCmd)
    def MenuKey(self):
        self.Execute(self.__MenuCmd)
    def MinusKey(self):
        self.Execute(self.__MinusCmd)
    def PlusKey(self):
        self.Execute(self.__PlusCmd)
    def PowerKey(self):
        self.Execute(self.__PowerCmd)
    def SourceKey(self):
        self.Execute(self.__SourceCmd)
    def FactoryKey(self):
        self.Execute(self.__FactoryCmd)

    def eventFilter(self, watched, event):
        if event.type() == QtCore.QEvent.KeyPress:
            keyEvent = QtGui.QKeyEvent(event)
            if self._serial.isOpen():
                if keyEvent.key() == QtCore.Qt.Key_W:
                    self.Execute(self.__ExitCmd)
                    print(Keymsg_1.isCustomize)
                    print(Keymsg_1.name)
                elif keyEvent.key() == QtCore.Qt.Key_S:
                    print(Keymsg_2.name)
                    self.Execute(self.__MenuCmd)
                elif keyEvent.key() == QtCore.Qt.Key_A:
                    self.Execute(self.__MinusCmd)
                elif keyEvent.key() == QtCore.Qt.Key_D:
                    self.Execute(self.__PlusCmd)
                elif keyEvent.key() == QtCore.Qt.Key_Z:
                    self._serial.send("iv ".encode())
                elif keyEvent.key() == QtCore.Qt.Key_X:
                    self._serial.send("iu".encode())
                elif keyEvent.key() == QtCore.Qt.Key_C:
                    self._serial.send("i ".encode())
            else:
                QtGui.QMessageBox.information(self, "Tips", "请先打开串口")
        if event.type() == QtCore.QEvent.KeyRelease:
            pass
            #print("the up key released")
        return QtGui.QWidget.eventFilter(self, watched, event)

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
