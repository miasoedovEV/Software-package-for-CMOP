# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design_window_add_sup_pump.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


class AddSupPumpDialog(object):
    def setupUi(self, Dialog, SupportPumpsTable, HELPING):
        Dialog.setObjectName("Dialog")
        Dialog.resize(760, 929)
        Dialog.setMaximumSize(QtCore.QSize(760, 929))
        self.label_pump_enter_2 = QtWidgets.QLabel(Dialog)
        self.label_pump_enter_2.setGeometry(QtCore.QRect(270, 0, 281, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.label_pump_enter_2.setFont(font)
        self.label_pump_enter_2.setObjectName("label_pump_enter_2")
        self.line_4 = QtWidgets.QFrame(Dialog)
        self.line_4.setGeometry(QtCore.QRect(-20, 40, 821, 5))
        self.line_4.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_4.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_4.setObjectName("line_4")
        self.add = QtWidgets.QPushButton(Dialog)
        self.add.setGeometry(QtCore.QRect(410, 240, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.add.setFont(font)
        self.add.setObjectName("add")
        self.retry = QtWidgets.QPushButton(Dialog)
        self.retry.setGeometry(QtCore.QRect(530, 240, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.retry.setFont(font)
        self.retry.setObjectName("retry")
        self.enter = QtWidgets.QPushButton(Dialog)
        self.enter.setGeometry(QtCore.QRect(650, 240, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.enter.setFont(font)
        self.enter.setObjectName("enter")
        self.line_3 = QtWidgets.QFrame(Dialog)
        self.line_3.setGeometry(QtCore.QRect(-10, 270, 821, 5))
        self.line_3.setFrameShape(QtWidgets.QFrame.HLine)
        self.line_3.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line_3.setObjectName("line_3")
        self.label_pump_enter = QtWidgets.QLabel(Dialog)
        self.label_pump_enter.setGeometry(QtCore.QRect(270, 290, 241, 41))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.label_pump_enter.setFont(font)
        self.label_pump_enter.setObjectName("label_pump_enter")
        self.tableWidget_pump_enter = QtWidgets.QTableWidget(Dialog)
        self.tableWidget_pump_enter.setGeometry(QtCore.QRect(55, 330, 677, 591))
        self.tableWidget_pump_enter.setObjectName("tableWidget_pump_enter")
        self.enter_table_data(SupportPumpsTable, HELPING)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setGeometry(QtCore.QRect(66, 60, 645, 171))
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(5)
        item = QtWidgets.QTableWidgetItem('Марка')
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem('D, мм')
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem('a')
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem('b')
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem('Qном')
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem('1')
        item.setFont(font)
        self.tableWidget.setRowCount(1)
        self.tableWidget.setVerticalHeaderItem(0, item)
        self.cancel_2 = QtWidgets.QPushButton(Dialog)
        self.cancel_2.setGeometry(QtCore.QRect(300, 240, 93, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        self.cancel_2.setFont(font)
        self.cancel_2.setObjectName("cancel_2")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def enter_table_data(self, SupportPumpsTable, HELPING):
        self.tableWidget_pump_enter.setRowCount(0)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.tableWidget_pump_enter.setColumnCount(5)
        item = QtWidgets.QTableWidgetItem('Марка')
        item.setFont(font)
        self.tableWidget_pump_enter.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem('Диаметр рабочего колеса')
        item.setFont(font)
        self.tableWidget_pump_enter.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem('a')
        item.setFont(font)
        self.tableWidget_pump_enter.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem('b')
        item.setFont(font)
        self.tableWidget_pump_enter.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem('Qном')
        item.setFont(font)
        self.tableWidget_pump_enter.setHorizontalHeaderItem(4, item)
        for index, pump in enumerate(SupportPumpsTable.select()):
            self.tableWidget_pump_enter.setRowCount(index + 1)
            item = QtWidgets.QTableWidgetItem(f'{index + 1}')
            item.setFont(font)
            item.setToolTip(HELPING)
            self.tableWidget_pump_enter.setVerticalHeaderItem(index, item)
            brand = QtWidgets.QTableWidgetItem(str(pump.brand))
            brand.setFont(font)
            self.tableWidget_pump_enter.setItem(index, 0, brand)
            impeller_diameter = QtWidgets.QTableWidgetItem(str(pump.impeller_diameter))
            impeller_diameter.setFont(font)
            impeller_diameter.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.tableWidget_pump_enter.setItem(index, 1, impeller_diameter)
            a = QtWidgets.QTableWidgetItem(str(pump.a))
            a.setFont(font)
            self.tableWidget_pump_enter.setItem(index, 2, a)
            b = QtWidgets.QTableWidgetItem(str(pump.b))
            b.setFont(font)
            self.tableWidget_pump_enter.setItem(index, 3, b)
            Qnom = QtWidgets.QTableWidgetItem(str(pump.Q_nom))
            Qnom.setFont(font)
            self.tableWidget_pump_enter.setItem(index, 4, Qnom)
        self.tableWidget_pump_enter.resizeColumnsToContents()
        self.tableWidget_pump_enter.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Добавление подпорного насоса"))
        self.label_pump_enter_2.setText(_translate("Dialog", "Добавление подпорного насоса"))
        self.add.setText(_translate("Dialog", "Добавить"))
        self.retry.setText(_translate("Dialog", "Сбросить"))
        self.enter.setText(_translate("Dialog", "Ввод"))
        self.label_pump_enter.setText(_translate("Dialog", "Список подпорных насосов"))
        self.cancel_2.setText(_translate("Dialog", "Отмена"))
