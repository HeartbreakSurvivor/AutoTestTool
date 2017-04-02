#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys,binascii
import importlib
importlib.reload(sys)

from MainWindow import Ui_MainWindow
from PyQt4 import QtCore, QtGui
from KeyMsg import KeyMsg
from serial import Serial
import serial.tools.list_ports
from MySerial import MySerial
from Command import *
from KeyControl import *
from keyedit import *
from serial.serialutil import SerialBase, SerialException, to_bytes, portNotOpenError, writeTimeoutError

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)


__author__ = "bigzhanghao"
__version__ = "0.1"

class MainWindow(QtGui.QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)

        QtCore.QCoreApplication.setOrganizationName("Cvte")
        QtCore.QCoreApplication.setOrganizationDomain("zhanghao3126@cvte.com")
        QtCore.QCoreApplication.setApplicationName("SerialTool")

        #variables definition
        self.KeyList = [
            QtCore.Qt.Key_A, QtCore.Qt.Key_B, QtCore.Qt.Key_C, QtCore.Qt.Key_D,
            QtCore.Qt.Key_E, QtCore.Qt.Key_F, QtCore.Qt.Key_G, QtCore.Qt.Key_H,
            QtCore.Qt.Key_I, QtCore.Qt.Key_J, QtCore.Qt.Key_K, QtCore.Qt.Key_L,
            QtCore.Qt.Key_M, QtCore.Qt.Key_N, QtCore.Qt.Key_O, QtCore.Qt.Key_P,
            QtCore.Qt.Key_Q, QtCore.Qt.Key_R, QtCore.Qt.Key_S, QtCore.Qt.Key_T,
            QtCore.Qt.Key_U, QtCore.Qt.Key_V, QtCore.Qt.Key_W, QtCore.Qt.Key_X,
            QtCore.Qt.Key_Y, QtCore.Qt.Key_Z]

        self.portlist = []
        self.__CommandList = []
        self._serial = MySerial()
        self.isopen = 0
        self._str = ""

        self.MainWindowInit()
        self.WriteSettings()
        self.ReadSettings()
        self.actionMstar_9570S.setChecked(True)

        self.AddSerialPorts()#serial configuration
        self.Signal_Slot_Init() # Setup the singal

        self.Command_Init()# The design pattern

    def MainWindowInit(self):
        self.setupUi(self)
        self.textEdit.setReadOnly(True)
        self.installEventFilter(self)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.Receive)

    def Signal_Slot_Init(self):
        self.ExitButton.connect(self.ExitButton, QtCore.SIGNAL('clicked()'), self.ExitKey)
        self.MenuButton.connect(self.MenuButton, QtCore.SIGNAL('clicked()'), self.MenuKey)
        self.MinusButton.connect(self.MinusButton, QtCore.SIGNAL('clicked()'), self.MinusKey)
        self.PlusButton.connect(self.PlusButton, QtCore.SIGNAL('clicked()'), self.PlusKey)
        self.PowerButton.connect(self.PowerButton, QtCore.SIGNAL('clicked()'), self.PowerKey)
        self.SourceButton.connect(self.SourceButton, QtCore.SIGNAL('clicked()'), self.SourceKey)
        self.FactoryButton.connect(self.FactoryButton, QtCore.SIGNAL('clicked()'), self.FactoryKey)

        self.SendDataButton.connect(self.SendDataButton, QtCore.SIGNAL('clicked()'), self.Send)
        self.ClearDataButton.connect(self.ClearDataButton, QtCore.SIGNAL('clicked()'), self.Clear)
        self.HexDisCheckbox.connect(self.HexDisCheckbox,QtCore.SIGNAL('clicked()'),self.DisHex)
        self.HexSendcheckBox_2.connect(self.HexSendcheckBox_2, QtCore.SIGNAL('clicked()'), self.SendHex)
        self.SaveDataButton.connect(self.SaveDataButton, QtCore.SIGNAL('clicked()'), self.Pause)

        self.actionMstar_9570S.connect(self.actionMstar_9570S, QtCore.SIGNAL('triggered()'), self.SelectChip)
        self.actionRealTek.connect(self.actionRealTek, QtCore.SIGNAL('triggered()'), self.SelectChip)

        self.actionKeyedit.connect(self.actionKeyedit,QtCore.SIGNAL('triggered()'),self.Edit_VirtualKey)
        # the serial settings
        self.menuConnect.connect(self.menuConnect, QtCore.SIGNAL('triggered()'), self.Switchserial)

        self.action4800.connect(self.action4800, QtCore.SIGNAL('triggered()'), self.Serial_SetBaudRate)
        self.action9600.connect(self.action9600, QtCore.SIGNAL('triggered()'), self.Serial_SetBaudRate)
        self.action57600.connect(self.action57600, QtCore.SIGNAL('triggered()'), self.Serial_SetBaudRate)
        self.action115200.connect(self.action115200, QtCore.SIGNAL('triggered()'), self.Serial_SetBaudRate)

        self.action5.connect(self.action5, QtCore.SIGNAL('triggered()'), self.Serial_SetDataBit)
        self.action6.connect(self.action6, QtCore.SIGNAL('triggered()'), self.Serial_SetDataBit)
        self.action7.connect(self.action7, QtCore.SIGNAL('triggered()'), self.Serial_SetDataBit)
        self.action8.connect(self.action8, QtCore.SIGNAL('triggered()'), self.Serial_SetDataBit)

        self.action1.connect(self.action1, QtCore.SIGNAL('triggered()'), self.Serial_SetStopBit)
        self.action1_5.connect(self.action1_5, QtCore.SIGNAL('triggered()'), self.Serial_SetStopBit)
        self.action3.connect(self.action3, QtCore.SIGNAL('triggered()'), self.Serial_SetStopBit)

        self.actionNone.connect(self.actionNone, QtCore.SIGNAL('triggered()'), self.Serial_SetParity)
        self.actionEven.connect(self.actionEven, QtCore.SIGNAL('triggered()'), self.Serial_SetParity)
        self.actionSpace.connect(self.actionSpace, QtCore.SIGNAL('triggered()'), self.Serial_SetParity)
        self.actionMark.connect(self.actionMark, QtCore.SIGNAL('triggered()'), self.Serial_SetParity)
        self.actionOdd.connect(self.actionOdd, QtCore.SIGNAL('triggered()'), self.Serial_SetParity)

    # add new command to the command list
    def SetCommands(self, Command):
        self.__CommandList.append(Command)

    #Createand set the commands
    def Command_Init(self):
        self.__MenuCmd = MeunCommand(self._serial)
        self.__ExitCmd = ExitCommand(self._serial)
        self.__PowerCmd = PowerCommand(self._serial)
        self.__PlusCmd = PlusCommand(self._serial)
        self.__MinusCmd = MinusCommand(self._serial)
        self.__SourceCmd = SourceCommand(self._serial)
        self.__FactoryCmd = FactoryCommand(self._serial)

        self.SetCommands(self.__ExitCmd)
        self.SetCommands(self.__MinusCmd)
        self.SetCommands(self.__PlusCmd)
        self.SetCommands(self.__MenuCmd)
        self.SetCommands(self.__PowerCmd)
        self.SetCommands(self.__SourceCmd)
        self.SetCommands(self.__FactoryCmd)

    #invoker execute the command
    def Execute(self,Command):
        if Command in self.__CommandList:
            Idx = self.__CommandList.index(Command)
            #Command.execute(self)
            self.__CommandList[Idx].execute(KeyMessage[Idx])

    def SelectChip(self):
        if self.GetChipSelect():
            print("chip selcect")
        else:
            print("select the mstar")

    def GetChipSelect(self):
        if self.actionRealTek.isChecked():
            return 1
        elif self.actionMstar_9570S.isChecked():
            return 0

    def Serial_SetBaudRate(self):
        if self.action4800.isChecked():
            self._serial.baudrate = 4800
        elif self.action9600.isChecked():
            self._serial.baudrate = 9600
        elif self.action57600.isChecked():
            self._serial.baudrate = 57600
        elif self.action115200.isChecked():
            self._serial.baudrate = 115200
        return self._serial.baudrate

    def Serial_SetDataBit(self):
        if self.action5.isChecked():
            self._serial.bytesize = 5
            print("5")
        elif self.action6.isChecked():
            self._serial.bytesize = 6
            print("6")
        elif self.action7.isChecked():
            self._serial.bytesize = 7
            print("7")
        elif self.action8.isChecked():
            self._serial.bytesize = 8
        return self._serial.bytesize

    def Serial_SetStopBit(self):
        if self.action1.isChecked():
            self._serial.stopbits = 1
            print("1")
        elif self.action1_5.isChecked():
            self._serial.stopbits = 1.5
            print("1.5")
        elif self.action3.isChecked():
            self._serial.stopbits = 2
        return self._serial.stopbits

    def Serial_SetParity(self):
        if self.actionNone.isChecked():
            self._serial.parity = 'N'
            print("none")
        elif self.actionOdd.isChecked():
            self._serial.parity = 'O'
            print("Odd")
        elif self.actionEven.isChecked():
            self._serial.parity = 'E'
            print("even")
        elif self.actionSpace.isChecked():
            self._serial.parity = 'S'
            print("space")
        elif self.actionMark.isChecked():
            self._serial.parity = 'M'
        return self._serial.parity

    def Edit_VirtualKey(self):
        KeyEditDialog = KeyEdit(self)  #QtGui.QDialog(self)# create a new dailog inherit from the parent Mainwindow
        KeyEditDialog.setModal(True)# set the new dialog with modal
        #KeyEditDialog.show()
        KeyEditDialog.exec_() #notice the difference of the show() and exec_(),the exec_() will wait until the user close the window
        self.ApplytheKeySettings()

        #KeyEditDialog = KeyEdit()
        #Ui_KeyEdit.setupUi(self,KeyEdit)
        #KeyEditDialog.show()

    def ApplytheKeySettings(self):
        self.ExitButton.setText(KeyMessage[0].getName())
        self.KeyIndicatorA.setText(KeyMessage[0].getEntityKey())

        self.MinusButton.setText(KeyMessage[1].getName())
        self.KeyIndicatorB.setText(KeyMessage[1].getEntityKey())

        self.PlusButton.setText(KeyMessage[2].getName())
        self.KeyIndicatorC.setText(KeyMessage[2].getEntityKey())

        self.MenuButton.setText(KeyMessage[3].getName())
        self.KeyIndicatorD.setText(KeyMessage[3].getEntityKey())

        self.PowerButton.setText(KeyMessage[4].getName())
        self.KeyIndicatorE.setText(KeyMessage[4].getEntityKey())

        self.SourceButton.setText(KeyMessage[5].getName())
        self.KeyIndicatorF.setText(KeyMessage[5].getEntityKey())

        self.FactoryButton.setText(KeyMessage[6].getName())
        self.KeyIndicatorG.setText(KeyMessage[6].getEntityKey())


    def ReadSettings(self):
        settings = QtCore.QSettings("bigzhanghao","MainWindow")

        if settings.value("ChipSet",0) == 0:
            self.actionMstar_9570S.setChecked(1)
        else:
            self.actionRealTek.setChecked(1)

        settings.beginGroup("Serial")
        if settings.value("BaudRate",9600) == 4800:
            self.action4800.setChecked(1)
        elif settings.value("BaudRate",9600) == 9600:
            self.action9600.setChecked(1)
        elif settings.value("BaudRate",9600) == 57600:
            self.action57600.setChecked(1)
        elif settings.value("BaudRate",9600) == 115200:
            self.action115200.setChecked(1)

        if settings.value("DataBits",8) == 5:
            self.action5.setChecked(1)
        elif settings.value("DataBits",8) == 6:
            self.action6.setChecked(1)
        elif settings.value("DataBits",8) == 7:
            self.action7.setChecked(1)
        elif settings.value("DataBits",8) == 8:
            self.action8.setChecked(1)

        if settings.value("StopBits", 1) == 1:
            self.action1.setChecked(1)
        elif settings.value("StopBits", 1) == 1.5:
            self.action1_5.setChecked(1)
        elif settings.value("StopBits", 1) == 2:
            self.action3.setChecked(1)

        if settings.value("Parity", "None") == "None":
            self.actionNone.setChecked(1)
        elif settings.value("Parity", "None") == "Odd":
            self.actionOdd.setChecked(1)
        elif settings.value("Parity", "None") == "Even":
            self.actionEven.setChecked(1)
        elif settings.value("Parity", "None") == "Mark":
            self.actionMark.setChecked(1)
        elif settings.value("Parity", "None") == "Space":
            self.actionSpace.setChecked(1)
        settings.endGroup()

        settings.beginGroup("KeyMsgGroup")
        settings.beginReadArray("KeyMessage")
        for i in range(KeyMessage.__len__()):
            settings.setArrayIndex(i)
            KeyMessage[i].setName(settings.value("keyname"))
            KeyMessage[i].setCustomize(settings.value("isCustomize"))
            KeyMessage[i].setEntityKey(settings.value("key"))
            KeyMessage[i].setContent(settings.value("content"))
            print(settings.value("keyname"))
            print(settings.value("key"))
            print(settings.value("isCustomize"))
        settings.endArray()
        settings.endGroup()

        self.ApplytheKeySettings()

    def WriteSettings(self):
        settings = QtCore.QSettings("bigzhanghao","MainWindow")

        settings.setValue("ChipSet",self.GetChipSelect())

        settings.beginGroup("Serial")
        settings.setValue("BaudRate",self.Serial_SetBaudRate())
        settings.setValue("DataBits", self.Serial_SetDataBit())
        settings.setValue("StopBits", self.Serial_SetStopBit())
        settings.setValue("Parity", self.Serial_SetParity())
        settings.endGroup()

        settings.beginGroup("KeyMsgGroup")
        settings.beginWriteArray("KeyMessage")
        for i in range(KeyMessage.__len__()):
            settings.setArrayIndex(i)
            settings.setValue("keyname",KeyMessage[i].getName())
            settings.setValue("isCustomize", KeyMessage[i].isCustomize)
            settings.setValue("key", KeyMessage[i].getEntityKey())
            settings.setValue("content", KeyMessage[i].getContent())
        settings.endArray()
        settings.endGroup()
    #actions
    def AddSerialPorts(self):
        self.port_list = self._serial.GetSerialPorts()
        self.PortActionGroup = QtGui.QActionGroup(self)
        self.PortActionGroup.setObjectName("PortActionGroup")
        if len(self.port_list):
            for x in self.port_list:
                tempName = x.device
                self.tempName = QtGui.QAction(tempName,self)
                self.tempName.setCheckable(True)
                self.PortList.addAction(self.tempName)
                self.PortActionGroup.addAction(self.tempName)
                self.portlist.append(self.tempName)
                print(self.tempName.text())
                #self.portlist.append(self.tempName)
            self.tempName.setChecked(True)
        else:
            QtGui.QMessageBox.information(self, "Tips", "没有找到可用的端口号")

    def GetCurrentPortNumber(self):
        for x in self.portlist:
            #assert isinstance(x.isChecked, object)
            if x.isChecked():
                return x.text()
        QtGui.QMessageBox.information(self, "Tips", "没有找到可用的端口号")

    def Switchserial(self):
        if self._serial.is_open:
            try:
                self._serial.close()
                self.timer.stop()
                self.isopen = 0
                self.menuConnect.setText(_translate("MainWindow", "ComPort Connect", None))
                self.PortList.setEnabled(True)
                self.menuBaudRates.setEnabled(True)
                self.menuData_Bits.setEnabled(True)
                self.menuStop_Bits.setEnabled(True)
                self.menuParity.setEnabled(True)
            except:
                QtGui.QMessageBox.information(self, "Tips", "串口关闭失败")
                sys.exit()
        else:
            try:
                portnumber = self.GetCurrentPortNumber()
                self._serial.port = portnumber #self.GetCurrentPortNumber()# "COM1"
                self._serial.open()
                self.timer.start(30)
                self.isopen = 1
                self.menuConnect.setText(_translate("MainWindow", "ComPort DisConnect", None))
                    #self.menuComPort.setEnabled(False)
                self.PortList.setEnabled(False)
                self.menuBaudRates.setEnabled(False)
                self.menuData_Bits.setEnabled(False)
                self.menuStop_Bits.setEnabled(False)
                self.menuParity.setEnabled(False)
                print("open the serial and timer start")
            except serial.serialutil.SerialException:
                QtGui.QMessageBox.information(self, "Tips", "串口打开失败，请确认串口号是否被占用")
                return False

    def Send(self):
        if not self._serial.is_open:
            QtGui.QMessageBox.information(self,"Tips","请先打开串口")
            return
        else:
            try:
                if not self.HexSendcheckBox.isChecked():
                    self._serial.send(self.DataToSend.text().encode())
                else:
                    self._serial.send(self.DataToSend.text().encode())
            except:
                print("send data fail")
                return

    def Receive(self):
        if self._serial.is_open:
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

    def Clear(self):
        self._str = ""
        self.textEdit.clear()
        self.DataToSend.clear()
        return

    def hexshow(argv):
        result = ''
        hLen = len(argv)
        for i in range(hLen):
            hvol = ord(argv[i])
            hhex = '%02x' % hvol
            result += hhex + ' '
            # print("hexshow: ", result)
        return result

    def Pause(self):
        if self.isopen:
            if self._serial.is_open:
                self._serial.close()
                self.timer.stop()
                self.SaveDataButton.setText(_translate("MainWindow", "开始", None))
            else:
                portnumber = self.GetCurrentPortNumber()
                self._serial.port = portnumber #self.GetCurrentPortNumber()# "COM1"
                self._serial.open()
                self.timer.start(30)
                self.SaveDataButton.setText(_translate("MainWindow", "暂停", None))
        else:
            print ("please open the serial")
            pass

    def DisHex(self):
        if self.HexDisCheckbox.isChecked():#check
#            temphex = hexshow(self._str)
            self.textEdit.clear()
#            self.textEdit.setText(temphex)
        else:#cancel check
            self.textEdit.clear()
            self.textEdit.setText(self._str)

    def SendHex(self):
        if self.HexSendcheckBox_2.isChecked():#check
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

    def GetSettingKey(self,index):
        for i in range(VirtualKeylist.__len__()):
            if KeyMessage[index].getEntityKey() == VirtualKeylist[i]:
                return self.KeyList[i]

    def eventFilter(self, watched, event):
        if event.type() == QtCore.QEvent.KeyPress:
            keyEvent = QtGui.QKeyEvent(event)
            if self._serial.isOpen():
                if keyEvent.key() == self.GetSettingKey(0):
                    self.Execute(self.__ExitCmd)
                elif keyEvent.key() == self.GetSettingKey(1):
                    self.Execute(self.__MinusCmd)
                elif keyEvent.key() == self.GetSettingKey(2):
                    self.Execute(self.__PlusCmd)
                elif keyEvent.key() == self.GetSettingKey(3):
                    self.Execute(self.__MenuCmd)
                elif keyEvent.key() == self.GetSettingKey(4):
                    self.Execute(self.__PowerCmd)
                elif keyEvent.key() == self.GetSettingKey(5):
                    self.Execute(self.__SourceCmd)
                elif keyEvent.key() == self.GetSettingKey(6):
                    self.Execute(self.__FactoryCmd)
            else:
                #QtGui.QMessageBox.information(self, "Tips", "请先打开串口")
                pass
        if event.type() == QtCore.QEvent.KeyRelease:
            pass
        return QtGui.QWidget.eventFilter(self, watched, event)

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
