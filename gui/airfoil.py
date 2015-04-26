# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'AirfoilDialog.ui'
#
# Created: Sat Apr 25 19:32:34 2015
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(363, 229)
        self.verticalLayout_2 = QtGui.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.dialog_clcr_inp = QtGui.QLineEdit(Dialog)
        self.dialog_clcr_inp.setMaximumSize(QtCore.QSize(100, 16777215))
        self.dialog_clcr_inp.setObjectName(_fromUtf8("dialog_clcr_inp"))
        self.gridLayout.addWidget(self.dialog_clcr_inp, 5, 1, 1, 1)
        self.dialog_cl_max_inp = QtGui.QLineEdit(Dialog)
        self.dialog_cl_max_inp.setMaximumSize(QtCore.QSize(100, 16777215))
        self.dialog_cl_max_inp.setObjectName(_fromUtf8("dialog_cl_max_inp"))
        self.gridLayout.addWidget(self.dialog_cl_max_inp, 2, 1, 1, 1)
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 2, 2, 1, 1)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        self.dialog_airfoil_name_comb = QtGui.QComboBox(Dialog)
        self.dialog_airfoil_name_comb.setObjectName(_fromUtf8("dialog_airfoil_name_comb"))
        self.dialog_airfoil_name_comb.addItem(_fromUtf8(""))
        self.gridLayout.addWidget(self.dialog_airfoil_name_comb, 0, 1, 1, 1)
        self.dialog_cl_cr_alpha_sb = QtGui.QSpinBox(Dialog)
        self.dialog_cl_cr_alpha_sb.setMaximum(30)
        self.dialog_cl_cr_alpha_sb.setObjectName(_fromUtf8("dialog_cl_cr_alpha_sb"))
        self.gridLayout.addWidget(self.dialog_cl_cr_alpha_sb, 5, 3, 1, 1)
        self.label_8 = QtGui.QLabel(Dialog)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 5, 4, 1, 1)
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 2, 4, 1, 1)
        self.label_7 = QtGui.QLabel(Dialog)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 5, 2, 1, 1)
        self.dialog_clmax_alpha_sb = QtGui.QSpinBox(Dialog)
        self.dialog_clmax_alpha_sb.setMaximum(30)
        self.dialog_clmax_alpha_sb.setObjectName(_fromUtf8("dialog_clmax_alpha_sb"))
        self.gridLayout.addWidget(self.dialog_clmax_alpha_sb, 2, 3, 1, 1)
        self.dialog_cdo_inp = QtGui.QLineEdit(Dialog)
        self.dialog_cdo_inp.setMaximumSize(QtCore.QSize(100, 16777215))
        self.dialog_cdo_inp.setObjectName(_fromUtf8("dialog_cdo_inp"))
        self.gridLayout.addWidget(self.dialog_cdo_inp, 6, 1, 1, 1)
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 6, 0, 1, 1)
        self.label_9 = QtGui.QLabel(Dialog)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 1, 0, 1, 1)
        self.dialog_tbyc_inp = QtGui.QLineEdit(Dialog)
        self.dialog_tbyc_inp.setMaximumSize(QtCore.QSize(100, 16777215))
        self.dialog_tbyc_inp.setObjectName(_fromUtf8("dialog_tbyc_inp"))
        self.gridLayout.addWidget(self.dialog_tbyc_inp, 1, 1, 1, 1)
        self.label_10 = QtGui.QLabel(Dialog)
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 1, 2, 1, 1)
        self.dialog_thick_loc_inp = QtGui.QLineEdit(Dialog)
        self.dialog_thick_loc_inp.setMaximumSize(QtCore.QSize(100, 16777215))
        self.dialog_thick_loc_inp.setObjectName(_fromUtf8("dialog_thick_loc_inp"))
        self.gridLayout.addWidget(self.dialog_thick_loc_inp, 1, 3, 1, 1)
        self.label_11 = QtGui.QLabel(Dialog)
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 7, 0, 1, 1)
        self.dialog_max_clcd_inp = QtGui.QLineEdit(Dialog)
        self.dialog_max_clcd_inp.setMaximumSize(QtCore.QSize(100, 16777215))
        self.dialog_max_clcd_inp.setObjectName(_fromUtf8("dialog_max_clcd_inp"))
        self.gridLayout.addWidget(self.dialog_max_clcd_inp, 7, 1, 1, 1)
        self.label_12 = QtGui.QLabel(Dialog)
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout.addWidget(self.label_12, 7, 2, 1, 1)
        self.dialog_max_clcd_alpha_sb = QtGui.QSpinBox(Dialog)
        self.dialog_max_clcd_alpha_sb.setMaximum(30)
        self.dialog_max_clcd_alpha_sb.setObjectName(_fromUtf8("dialog_max_clcd_alpha_sb"))
        self.gridLayout.addWidget(self.dialog_max_clcd_alpha_sb, 7, 3, 1, 1)
        self.label_13 = QtGui.QLabel(Dialog)
        self.label_13.setObjectName(_fromUtf8("label_13"))
        self.gridLayout.addWidget(self.label_13, 7, 4, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout_2.addWidget(self.buttonBox)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.label.setText(_translate("Dialog", "Airfoil Name:", None))
        self.label_2.setText(_translate("Dialog", "CLmax", None))
        self.label_5.setText(_translate("Dialog", "at alpha", None))
        self.label_3.setText(_translate("Dialog", "CLcruise", None))
        self.dialog_airfoil_name_comb.setItemText(0, _translate("Dialog", "None", None))
        self.label_8.setText(_translate("Dialog", "[deg]", None))
        self.label_6.setText(_translate("Dialog", "[deg]", None))
        self.label_7.setText(_translate("Dialog", "at alpha", None))
        self.label_4.setText(_translate("Dialog", "Cd0", None))
        self.label_9.setText(_translate("Dialog", "Airfoil t/c:", None))
        self.label_10.setText(_translate("Dialog", "Location %", None))
        self.label_11.setText(_translate("Dialog", "Max. Cl/Cd", None))
        self.label_12.setText(_translate("Dialog", "at alpha", None))
        self.label_13.setText(_translate("Dialog", "[deg]", None))

