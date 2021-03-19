# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design_enter_diametre_pipe.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from settings import get_source_dict


class PipeDnDialog(object):
    def setupUi(self, Dialog, var):
        Dialog.setObjectName("Dialog")
        Dialog.resize(620, 239)
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 30, 441, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 60, 671, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(20, 90, 671, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(20, 120, 671, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(11)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.label_Dn = QtWidgets.QLabel(Dialog)
        self.label_Dn.setGeometry(QtCore.QRect(20, 160, 181, 16))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.label_Dn.setFont(font)
        self.label_Dn.setObjectName("label_Dn")
        self.lineEdit_7 = QtWidgets.QLineEdit(Dialog)
        self.lineEdit_7.setGeometry(QtCore.QRect(200, 151, 113, 31))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.next = QtWidgets.QPushButton(Dialog)
        self.next.setGeometry(QtCore.QRect(502, 200, 101, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.next.setFont(font)
        self.next.setObjectName("next")
        self.enter = QtWidgets.QPushButton(Dialog)
        self.enter.setGeometry(QtCore.QRect(390, 200, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.enter.setFont(font)
        self.enter.setObjectName("enter")
        self.retry = QtWidgets.QPushButton(Dialog)
        self.retry.setGeometry(QtCore.QRect(280, 200, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.retry.setFont(font)
        self.retry.setObjectName("retry")

        self.retranslateUi(Dialog, var)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog, var):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        dict_value = get_source_dict(var)
        self.label.setText(_translate("Dialog", f"Расчётный наружный диаметр трубы составил: {int(dict_value['Dn'])} мм."))
        self.label_2.setText(
            _translate("Dialog", "Если вы хотите продолжить расчёт нажимете \"Продолжить\". Если вы хотите"))
        self.label_3.setText(
            _translate("Dialog", "продолжить расчёт с пользовательским диаметром, введите диаметр в поле"))
        self.label_4.setText(_translate("Dialog", "ввода и нажмите \"Ввод\"."))
        self.label_Dn.setText(_translate("Dialog", "Наружный диаметр, мм:"))
        self.next.setText(_translate("Dialog", "Продолжить"))
        self.enter.setText(_translate("Dialog", "Ввод"))
        self.retry.setText(_translate("Dialog", "Сбросить"))
