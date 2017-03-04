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

import keyedit
from serial.serialutil import SerialBase, SerialException, to_bytes, portNotOpenError, writeTimeoutError

__author__ = "bigzhanghao"
__version__ = "0.1"


class MainWindow(QtGui.QMainWindow,Ui_MainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)

        QtCore.QCoreApplication.setOrganizationName("Cvte");
        QtCore.QCoreApplication.setOrganizationDomain("zhanghao3126@cvte.com");
        QtCore.QCoreApplication.setApplicationName("SerialTool");

        #variables definition
        self.__CommandList = []
        self._serial = MySerial()
        self._str = ""

        self.MainWindowInit()
        self.ReadSettings()

        self._serial.GetSerialPorts()#serial configuration
        self.Signal_Slot_Init() # Setup the singal

        self.Command_Init()# The design pattern
    """
        Keymsg_1.setName("Exit")
        Keymsg_2.setName("Minus")
        Keymsg_3.setName("Plus")
        Keymsg_4.setName("Menu")
        Keymsg_5.setName("Power")
        Keymsg_6.setName("Source")
        Keymsg_7.setName("Factory")
    """

    def MainWindowInit(self):
        self.setupUi(self)
        self.textEdit.setReadOnly(True)
        self.installEventFilter(self)
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.Receive)
        pass

    def Signal_Slot_Init(self):
        self.ExitButton.connect(self.ExitButton, QtCore.SIGNAL('clicked()'), self.ExitKey)
        self.MenuButton.connect(self.MenuButton, QtCore.SIGNAL('clicked()'), self.MenuKey)
        self.MinusButton.connect(self.MinusButton, QtCore.SIGNAL('clicked()'), self.MinusKey)
        self.PlusButton.connect(self.PlusButton, QtCore.SIGNAL('clicked()'), self.PlusKey)
        self.PowerButton.connect(self.MenuButton, QtCore.SIGNAL('clicked()'), self.PowerKey)
        self.SourceButton.connect(self.MinusButton, QtCore.SIGNAL('clicked()'), self.SourceKey)
        self.FactoryButton.connect(self.PlusButton, QtCore.SIGNAL('clicked()'), self.FactoryKey)

        self.SendDataButton.connect(self.SendDataButton, QtCore.SIGNAL('clicked()'), self.Send)
        self.ClearDataButton.connect(self.ClearDataButton, QtCore.SIGNAL('clicked()'), self.Clear)
        self.HexDisCheckbox.connect(self.HexDisCheckbox,QtCore.SIGNAL('clicked()'),self.DisHex)
        self.HexSendcheckBox_2.connect(self.HexSendcheckBox_2, QtCore.SIGNAL('clicked()'), self.SendHex)
        self.SaveDataButton.connect(self.SaveDataButton, QtCore.SIGNAL('clicked()'), self.SaveAs)

        self.actionMstar_9570S.connect(self.actionMstar_9570S, QtCore.SIGNAL('triggered()'), self.SelectChip)
        self.actionRealTek.connect(self.actionRealTek, QtCore.SIGNAL('triggered()'), self.SelectChip)

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

    #invoker execute the command
    def Execute(self,Command):
        if Command in self.__CommandList:
            Idx = self.__CommandList.index(Command)
            print(Idx)
            #Command.execute(self)
            self.__CommandList[Idx].execute()


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
            print("4800")
        if self.action9600.isChecked():
            self._serial.baudrate = 9600
            print("6998")
        if self.action57600.isChecked():
            self._serial.baudrate = 57600
            print("123127")
        if self.action115200.isChecked():
            self._serial.baudrate = 115200
            print("812321")

    def Serial_SetDataBit(self):
        if self.action5.isChecked():
            self._serial.bytesize = 5
            print("5")
        if self.action6.isChecked():
            self._serial.bytesize = 6
            print("6")
        if self.action7.isChecked():
            self._serial.bytesize = 7
            print("7")
        if self.action8.isChecked():
            self._serial.bytesize = 8
            print("8")

    def Serial_SetStopBit(self):
        if self.action1.isChecked():
            self._serial.stopbits = 1
            print("1")
        if self.action1_5.isChecked():
            self._serial.stopbits = 1.5
            print("1.5")
        if self.action3.isChecked():
            self._serial.stopbits = 2
            print("2")

    def Serial_SetParity(self):
        if self.actionNone.isChecked():
            self._serial.parity = 'N'
            print("none")
        if self.actionOdd.isChecked():
            self._serial.parity = 'O'
            print("Odd")
        if self.actionEven.isChecked():
            self._serial.parity = 'E'
            print("even")
        if self.actionSpace.isChecked():
            self._serial.parity = 'S'
            print("space")
        if self.actionMark.isChecked():
            self._serial.parity = 'M'
            print("mark")


    def ReadSettings(self):
        settings = QtCore.QSettings()
        if settings.value("ChipSet",0):
            print("here?2")
            self.actionRealTek.setChecked(1)
        else:
            print("here?1")
            self.actionMstar_9570S.setChecked(1)


    def WriteSettings(self):
        settings = QtCore.QSettings()
        #settings.setValue("ChipSet",QtCore.QVariant(self.GetChipSelect()))
        settings.setValue("ChipSet",1)
        pass

    #actions
    def GetSerialPorts(self):
        port_list = self._serial.GetSerialPorts()
        if len(port_list):
            for x in port_list:
                self.menuComPort.addQAction(x.device)
        else:
            print("Can't find serial port")
            pass

    def Switchserial(self):
        if self._serial.is_open:
            try:
                self._serial.close()
                self.timer.stop()

                self.menuConnect.setText(_translate("MainWindow", "ComPort Connect", None))
                self.menuComPort.setEnabled(True)
                self.menuBaudRates.setEnabled(True)
                self.menuData_Bits.setEnabled(True)
                self.menuStop_Bits.setEnabled(True)
                self.menuParity.setEnabled(True)
            except:
                print("close the serial fail")
        else:
            try:
                self._serial.open()
                self.timer.start(30)
                self.menuConnect.setText(_translate("MainWindow", "ComPort DisConnect", None))
                self.menuComPort.setEnabled(False)
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

    def DisHex(self):
        if self.HexDisCheckbox.isChecked():#check
            temphex = hexshow(self._str)
            self.textEdit.clear()
            self.textEdit.setText(temphex)
        else:#cancel check
            self.textEdit.clear()
            self.textEdit.setText(self._str)

    def SaveAs(self):
        self.DataToSend.clear()
        if self.HexSendcheckBox.isChecked():#check
            print("Send Hex checked")
        else:# cancel check
            print("Send Hex no checked")

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
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
