# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainboard.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

class Ui_UsartTool(object):
    def setupUi(self, UsartTool):
        UsartTool.setObjectName(_fromUtf8("UsartTool"))
        UsartTool.resize(472, 323)
        self.pushButton = QtGui.QPushButton(UsartTool)
        self.pushButton.setGeometry(QtCore.QRect(20, 270, 75, 23))
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.pushButton_2 = QtGui.QPushButton(UsartTool)
        self.pushButton_2.setGeometry(QtCore.QRect(140, 270, 75, 23))
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.layoutWidget = QtGui.QWidget(UsartTool)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 20, 91, 211))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(self.layoutWidget)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout.addWidget(self.label_3)
        self.label_2 = QtGui.QLabel(self.layoutWidget)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout.addWidget(self.label_2)
        self.label_4 = QtGui.QLabel(self.layoutWidget)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout.addWidget(self.label_4)
        self.label_5 = QtGui.QLabel(self.layoutWidget)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.verticalLayout.addWidget(self.label_5)
        self.textEdit = QtGui.QTextEdit(UsartTool)
        self.textEdit.setGeometry(QtCore.QRect(270, 40, 191, 111))
        self.textEdit.setObjectName(_fromUtf8("textEdit"))
        self.label_6 = QtGui.QLabel(UsartTool)
        self.label_6.setGeometry(QtCore.QRect(270, 10, 121, 21))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.label_7 = QtGui.QLabel(UsartTool)
        self.label_7.setGeometry(QtCore.QRect(270, 170, 81, 31))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.pushButton_3 = QtGui.QPushButton(UsartTool)
        self.pushButton_3.setGeometry(QtCore.QRect(270, 270, 75, 23))
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.pushButton_4 = QtGui.QPushButton(UsartTool)
        self.pushButton_4.setGeometry(QtCore.QRect(370, 270, 75, 23))
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.lineEdit = QtGui.QLineEdit(UsartTool)
        self.lineEdit.setGeometry(QtCore.QRect(270, 210, 191, 31))
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.widget = QtGui.QWidget(UsartTool)
        self.widget.setGeometry(QtCore.QRect(130, 10, 111, 231))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.comboBox = QtGui.QComboBox(self.widget)
        self.comboBox.setObjectName(_fromUtf8("comboBox"))
        self.verticalLayout_2.addWidget(self.comboBox)
        self.comboBox_2 = QtGui.QComboBox(self.widget)
        self.comboBox_2.setObjectName(_fromUtf8("comboBox_2"))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.comboBox_2.addItem(_fromUtf8(""))
        self.verticalLayout_2.addWidget(self.comboBox_2)
        self.comboBox_3 = QtGui.QComboBox(self.widget)
        self.comboBox_3.setObjectName(_fromUtf8("comboBox_3"))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.comboBox_3.addItem(_fromUtf8(""))
        self.verticalLayout_2.addWidget(self.comboBox_3)
        self.comboBox_4 = QtGui.QComboBox(self.widget)
        self.comboBox_4.setObjectName(_fromUtf8("comboBox_4"))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.comboBox_4.addItem(_fromUtf8(""))
        self.verticalLayout_2.addWidget(self.comboBox_4)
        self.comboBox_5 = QtGui.QComboBox(self.widget)
        self.comboBox_5.setObjectName(_fromUtf8("comboBox_5"))
        self.comboBox_5.addItem(_fromUtf8(""))
        self.comboBox_5.addItem(_fromUtf8(""))
        self.comboBox_5.addItem(_fromUtf8(""))
        self.comboBox_5.addItem(_fromUtf8(""))
        self.comboBox_5.addItem(_fromUtf8(""))
        self.verticalLayout_2.addWidget(self.comboBox_5)
        self.layoutWidget.raise_()
        self.pushButton.raise_()
        self.pushButton_2.raise_()
        self.comboBox.raise_()
        self.comboBox_2.raise_()
        self.comboBox_3.raise_()
        self.comboBox_4.raise_()
        self.comboBox_5.raise_()
        self.textEdit.raise_()
        self.label_6.raise_()
        self.label_7.raise_()
        self.pushButton_3.raise_()
        self.pushButton_4.raise_()
        self.lineEdit.raise_()

        self.retranslateUi(UsartTool)
        #QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("pressed()")), self.textEdit.close)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("pressed()")), self.buttonclick)
        self.clickCnt = 0
        QtCore.QObject.connect(self.pushButton_4, QtCore.SIGNAL(_fromUtf8("clicked()")), UsartTool.close)
        QtCore.QMetaObject.connectSlotsByName(UsartTool)

    def retranslateUi(self, UsartTool):
        UsartTool.setWindowTitle(_translate("UsartTool", "Dialog", None))
        self.pushButton.setText(_translate("UsartTool", "打开串口", None))
        self.pushButton_2.setText(_translate("UsartTool", "关闭串口", None))
        self.label.setText(_translate("UsartTool", "串口号：", None))
        self.label_3.setText(_translate("UsartTool", "数据位：", None))
        self.label_2.setText(_translate("UsartTool", "波特率：", None))
        self.label_4.setText(_translate("UsartTool", "停止位：", None))
        self.label_5.setText(_translate("UsartTool", "奇偶校验位：", None))
        self.label_6.setText(_translate("UsartTool", "数据接收区域：", None))
        self.label_7.setText(_translate("UsartTool", "数据发送区域：", None))
        self.pushButton_3.setText(_translate("UsartTool", "发送", None))
        self.pushButton_4.setText(_translate("UsartTool", "清除", None))
        self.comboBox_2.setItemText(0, _translate("UsartTool", "5", None))
        self.comboBox_2.setItemText(1, _translate("UsartTool", "6", None))
        self.comboBox_2.setItemText(2, _translate("UsartTool", "7", None))
        self.comboBox_2.setItemText(3, _translate("UsartTool", "8", None))
        self.comboBox_3.setItemText(0, _translate("UsartTool", "4800", None))
        self.comboBox_3.setItemText(1, _translate("UsartTool", "9600", None))
        self.comboBox_3.setItemText(2, _translate("UsartTool", "19200", None))
        self.comboBox_3.setItemText(3, _translate("UsartTool", "57600", None))
        self.comboBox_3.setItemText(4, _translate("UsartTool", "115200", None))
        self.comboBox_4.setItemText(0, _translate("UsartTool", "1", None))
        self.comboBox_4.setItemText(1, _translate("UsartTool", "1.5", None))
        self.comboBox_4.setItemText(2, _translate("UsartTool", "2", None))
        self.comboBox_5.setItemText(0, _translate("UsartTool", "None", None))
        self.comboBox_5.setItemText(1, _translate("UsartTool", "Odd", None))
        self.comboBox_5.setItemText(2, _translate("UsartTool", "Even", None))
        self.comboBox_5.setItemText(3, _translate("UsartTool", "Mark", None))
        self.comboBox_5.setItemText(4, _translate("UsartTool", "Space", None))

    def buttonclick(self):
        self.clickCnt+=1
        _translate = QtCore.QCoreApplication.translate
        self.textEdit.setText(_translate("UsartTool","click cnt:%d"%self.clickCnt))



