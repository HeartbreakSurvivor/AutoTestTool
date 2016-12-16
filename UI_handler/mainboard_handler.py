#-*- coding: utf-8 -*-

from time import ctime
from mainboard import Ui_UsartTool as Mymainboard

class ui_handler(Mymainboard):
    def __init__(self,parent=None):
        Mymainboard.__init__(self)

    def _PortOpen(self):
        self.pushButton.setText("Close")

    def _PortClose(self):
        self.pushButton_2.setText("Open")

    def onSendData(self, data=None, _type="ascii"):
        if not data: data = self.lineEdit.toPlainText()
        if _type == "hex":
            data = ''.join(data.split())
            data = ' '.join([data[i:i+2] for i in xrange(0, len(data), 2)]).upper()
        else:
            data = data.replace('\n', '<br/>')
        self.lineEdit.append('<b>Send</b> @%s<br/><font color="white">%s</font><br/><br/>'
                                    % (ctime(), data))
        self.lineEdit.clear()
    def _ClearContent(self):
        self.textEdit.clear()