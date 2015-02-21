# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'E:\Acads\BTP\OpAiDe\gui\window.ui'
#
# Created: Mon Feb 09 09:40:57 2015
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName(_fromUtf8("MainWindow"))
        MainWindow.resize(382, 296)
        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName(_fromUtf8("centralwidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.pass_label = QtGui.QLabel(self.centralwidget)
        self.pass_label.setObjectName(_fromUtf8("pass_label"))
        self.horizontalLayout_2.addWidget(self.pass_label)
        self.wt_estimate_label = QtGui.QLabel(self.centralwidget)
        self.wt_estimate_label.setObjectName(_fromUtf8("wt_estimate_label"))
        self.horizontalLayout_2.addWidget(self.wt_estimate_label)
        self.verticalLayout_6.addLayout(self.horizontalLayout_2)
        self.verticalLayout.addLayout(self.verticalLayout_6)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout.addLayout(self.verticalLayout_4)
        self.min_pass = QtGui.QLabel(self.centralwidget)
        self.min_pass.setObjectName(_fromUtf8("min_pass"))
        self.horizontalLayout.addWidget(self.min_pass)
        self.pass_slider = QtGui.QSlider(self.centralwidget)
        self.pass_slider.setMaximum(100)
        self.pass_slider.setSingleStep(10)
        self.pass_slider.setOrientation(QtCore.Qt.Horizontal)
        self.pass_slider.setObjectName(_fromUtf8("pass_slider"))
        self.horizontalLayout.addWidget(self.pass_slider)
        self.max_pass = QtGui.QLabel(self.centralwidget)
        self.max_pass.setObjectName(_fromUtf8("max_pass"))
        self.horizontalLayout.addWidget(self.max_pass)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 382, 21))
        self.menubar.setObjectName(_fromUtf8("menubar"))
        self.menuFile = QtGui.QMenu(self.menubar)
        self.menuFile.setObjectName(_fromUtf8("menuFile"))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName(_fromUtf8("statusbar"))
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QObject.connect(self.pass_slider, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), self.wt_estimate_label.update)
        QtCore.QObject.connect(self.min_pass, QtCore.SIGNAL(_fromUtf8("linkActivated(QString)")), self.wt_estimate_label.setText)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow", None))
        self.pass_label.setText(_translate("MainWindow", "Passengers: ", None))
        self.wt_estimate_label.setText(_translate("MainWindow", "Estimated Gross_weight:", None))
        self.min_pass.setText(_translate("MainWindow", "Min Pass", None))
        self.max_pass.setText(_translate("MainWindow", "Max Pass", None))
        self.menuFile.setTitle(_translate("MainWindow", "File", None))

