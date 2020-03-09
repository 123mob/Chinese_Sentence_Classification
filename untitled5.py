# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'untitled5.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("句子分析")
        Dialog.resize(400, 300)
        self.input = QtWidgets.QLineEdit(Dialog)
        self.input.setGeometry(QtCore.QRect(40, 40, 321, 31))
        self.input.setObjectName("input")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 81, 20))
        self.label.setObjectName("label")
        self.activityButton = QtWidgets.QPushButton(Dialog)
        self.activityButton.setGeometry(QtCore.QRect(150, 90, 101, 41))
        self.activityButton.setObjectName("activityButton")
        self.output = QtWidgets.QTextEdit(Dialog)
        self.output.setGeometry(QtCore.QRect(40, 160, 321, 111))
        self.output.setObjectName("output")

        self.retranslateUi(Dialog)
        self.activityButton.clicked.connect(Dialog.activity)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "请输入一个句子"))
        self.activityButton.setText(_translate("Dialog", "分析句子"))
