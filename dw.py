# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dw.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        self.line = QtWidgets.QLineEdit(Form)
        self.line.setGeometry(QtCore.QRect(2, 29, 351, 21))
        self.line.setObjectName("line")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(0, 0, 341, 21))
        font = QtGui.QFont()
        font.setPointSize(20)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setGeometry(QtCore.QRect(0, 90, 171, 41))
        self.pushButton.setObjectName("pushButton")
        self.line_2 = QtWidgets.QLineEdit(Form)
        self.line_2.setGeometry(QtCore.QRect(0, 60, 351, 21))
        self.line_2.setObjectName("line_2")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "Paste u\'r YT link"))
        self.pushButton.setText(_translate("Form", "Download"))

