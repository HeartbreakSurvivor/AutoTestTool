#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
#from mainboard import Ui_UsartTool
#import UI.mainboard
from mainboard import Ui_UsartTool
from PyQt4 import QtCore, QtGui

__author__ = "bigzhanghao"
__version__ = "0.1"

if __name__ == "__main__":
    print(__name__)
    print(__author__)
    print(__version__)
    app = QtGui.QApplication(sys.argv)
    UsartTool = QtGui.QDialog()
    ui = Ui_UsartTool()
    ui.setupUi(UsartTool)
    UsartTool.show()
    sys.exit(app.exec_())
