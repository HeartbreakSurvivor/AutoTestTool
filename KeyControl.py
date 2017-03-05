from PyQt4 import QtCore, QtGui
from KeyMsg import KeyMsg
from keyedit import Ui_KeyEdit

global Keymsg_1 , Keymsg_2 , Keymsg_3 , Keymsg_4 , Keymsg_5 , Keymsg_6 , Keymsg_7
Keymsg_1 = KeyMsg()
Keymsg_2 = KeyMsg()
Keymsg_3 = KeyMsg()
Keymsg_4 = KeyMsg()
Keymsg_5 = KeyMsg()
Keymsg_6 = KeyMsg()
Keymsg_7 = KeyMsg()

KeyMessage = [Keymsg_1, Keymsg_2, Keymsg_3, Keymsg_4, Keymsg_5, Keymsg_6, Keymsg_7]

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
