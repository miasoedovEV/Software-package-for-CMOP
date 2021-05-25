# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design_save_error_xls.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class ErrorXlsDialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(584, 169)
        Dialog.setMaximumSize(QtCore.QSize(584, 172))
        self.gridLayout = QtWidgets.QGridLayout(Dialog)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(12)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_3 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.verticalLayout.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName("label_4")
        self.verticalLayout.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(self.frame)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.label_5.setFont(font)
        self.label_5.setAlignment(QtCore.Qt.AlignCenter)
        self.label_5.setObjectName("label_5")
        self.verticalLayout.addWidget(self.label_5)
        self.Ok = QtWidgets.QFrame(self.frame)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.Ok.setFont(font)
        self.Ok.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.Ok.setFrameShadow(QtWidgets.QFrame.Raised)
        self.Ok.setObjectName("Ok")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.Ok)
        self.gridLayout_2.setContentsMargins(450, -1, -1, -1)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton = QtWidgets.QPushButton(self.Ok)
        self.pushButton.setObjectName("pushButton")
        self.pushButton.setFont(font)
        self.gridLayout_2.addWidget(self.pushButton, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.Ok)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Ошибка вывода в xls"))
        self.label_3.setText(_translate("Dialog", "Ошибка"))
        self.label_4.setText(_translate("Dialog", "Выбранный объект не является папкой."))
        self.label_5.setText(_translate("Dialog", "Выберете другой объект, являющийся папкой."))
        self.pushButton.setText(_translate("Dialog", "Ок"))
