import sys
import mywindow
from PyQt4 import QtGui, uic, QtCore

app = QtGui.QApplication(sys.argv)
win = mywindow.MyWindow()
sys.exit(app.exec_())
