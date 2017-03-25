from PyQt4 import QtCore, QtGui
from KeyMsg import KeyMsg
from keyedit import Ui_KeyEdit
from main import MainWindow
from MainWindow import Ui_MainWindow

"""the Model--the MVC pattern"""
global Keymsg_1 , Keymsg_2 , Keymsg_3 ,Keymsg_4 , Keymsg_5 , Keymsg_6 , Keymsg_7
Keymsg_1 = KeyMsg("Exit","G","",0)
Keymsg_2 = KeyMsg("Minus","Q","",0)
Keymsg_3 = KeyMsg("Plus","S","",0)
Keymsg_4 = KeyMsg("Menu","D","",0)
Keymsg_5 = KeyMsg("Power","B","",0)
Keymsg_6 = KeyMsg("Source","X","",0)
Keymsg_7 = KeyMsg("Factory","L","",0)

KeyMessage = [Keymsg_1, Keymsg_2, Keymsg_3, Keymsg_4, Keymsg_5, Keymsg_6, Keymsg_7]

VirtualKeylist = ["A", "B", "C", "D", "E", "F",
                       "G", "H", "I", "J", "K", "L",
                       "M", "N", "O", "P", "Q", "R",
                       "S", "T", "U", "V", "W", "X",
                       "Y", "Z"]
try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

class KeyEdit(QtGui.QDialog,Ui_KeyEdit):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.setupUi(self)

        self.__KeyName = [self.KeyName1,self.KeyName2,self.KeyName3,self.KeyName4,
                              self.KeyName5,self.KeyName6,self.KeyName7]
        self.__Customize = [self.KeyCustome1,self.KeyCustome2,self.KeyCustome3,self.KeyCustome4,
                                self.KeyCustome5,self.KeyCustome6,self.KeyCustome7]
        self.__Content = [self.SendMsg1,self.SendMsg2,self.SendMsg3,self.SendMsg4,self.SendMsg5,
                              self.SendMsg6,self.SendMsg7]
        self.__VirtualKey = [self.VirtualKey1,self.VirtualKey2,self.VirtualKey3,self.VirtualKey4,
                                self.VirtualKey5,self.VirtualKey6,self.VirtualKey7]

        self.KeyCustome1.connect(self.KeyCustome1, QtCore.SIGNAL('clicked()'), self.IsCustomized)
        self.KeyCustome2.connect(self.KeyCustome2, QtCore.SIGNAL('clicked()'), self.IsCustomized)
        self.KeyCustome3.connect(self.KeyCustome3, QtCore.SIGNAL('clicked()'), self.IsCustomized)
        self.KeyCustome4.connect(self.KeyCustome4, QtCore.SIGNAL('clicked()'), self.IsCustomized)
        self.KeyCustome5.connect(self.KeyCustome5, QtCore.SIGNAL('clicked()'), self.IsCustomized)
        self.KeyCustome6.connect(self.KeyCustome6, QtCore.SIGNAL('clicked()'), self.IsCustomized)
        self.KeyCustome7.connect(self.KeyCustome7, QtCore.SIGNAL('clicked()'), self.IsCustomized)

        #self.buttonBox.connect(self.buttonBox, QtCore.SIGNAL('clicked()'), self.closeEvent)
        #self.buttonBox.accepted.connect(self.closeEvent)
        #self.buttonBox.rejected.connect(self.closeEvent)
        #QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")),self.closeEvent)
        self.buttonBox.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")),self.savesettings)

        for i in range(VirtualKeylist.__len__()):
            for j in range(self.__VirtualKey.__len__()):
                self.__VirtualKey[j].insertItem(i, VirtualKeylist[i])

        for i in range(KeyMessage.__len__()):
            self.__KeyName[i].setText(_fromUtf8(KeyMessage[i].getName()))
            self.__KeyName[i].setMaxLength(10)
            self.__KeyName[i].setAlignment(QtCore.Qt.AlignCenter)

            print(KeyMessage[i].isCustomizeOrnot())
            if KeyMessage[i].isCustomizeOrnot():
                self.__Customize[i].setChecked(True)
                if KeyMessage[i].getContent():
                    self.__Content[i].setText(_fromUtf8(KeyMessage[i].getContent()))
            else:
                self.__Customize[i].setChecked(False)
                if KeyMessage[i].getContent():
                    self.__Content[i].setText(_fromUtf8(KeyMessage[i].getContent()))
                self.__Content[i].setReadOnly(True)

            for j in range(26):
                if KeyMessage[i].getEntityKey() == VirtualKeylist[j]:
                    self.__VirtualKey[i].setCurrentIndex(j)

        #self.GetEntityKey()
    def savesettings(self):
        print("close the wssindow")
        self.IsCustomized()
        self.GetEntityKey()
        self.GetKeyName()
        self.GetSendMsg()

        self.close()

    def closeEvent(self,QCloseEvent):
        pass
        #print("close the window")
        #MainWindow.ApplytheKeySettings()

    def IsCustomized(self):
        for i in range(self.__Customize.__len__()):
            if self.__Customize[i].isChecked():
                KeyMessage[i].isCustomize = 1
                self.__Content[i].setReadOnly(False)
            else:
                KeyMessage[i].isCustomize = 0
                self.__Content[i].setReadOnly(True)

    def GetEntityKey(self):
        for i in range(self.__VirtualKey.__len__()):
            if self.__VirtualKey.count(self.__VirtualKey[i].currentText()) > 1:
                QtGui.QMessageBox.information(self, "Tips", "定义了相同的按键")
                break
            if self.__VirtualKey[i].currentText() is not None:
                KeyMessage[i].setEntityKey(self.__VirtualKey[i].currentText())

    def GetSendMsg(self):
        for i in range(self.__Content.__len__()):
            if self.__Customize[i].isChecked():
                TempMsg = self.__Content[i].text()
                KeyMessage[i].setContent(TempMsg)

    def GetKeyName(self):
        for i in range(self.__KeyName.__len__()):
            #if self.__KeyName[i].Length() >= 10:
            #    print("what's time")
            KeyMessage[i].setName(self.__KeyName[i].text())
