# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'designer_window_list_kaf.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

HELPING = 'Кликните правой кнопкой кнопкой мыши по строчке коэффициента, который хотите выбрать. '


class WindowKafList(object):
    def setupUi(self, MainWindow, DataOddsTable):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(699, 763)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.frame)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.frame_2)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.label = QtWidgets.QLabel(self.frame_2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_2.addWidget(self.label, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(self.frame)
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_3)
        self.gridLayout_3.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_3.setSpacing(0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tableWidget = QtWidgets.QTableWidget(self.frame_3)
        self.tableWidget.setObjectName("tableWidget")
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        item = QtWidgets.QTableWidgetItem('Наименование коэффициента')
        item.setFont(font)
        self.tableWidget.setColumnCount(3)
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem('Причина')
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem('Значение')
        item.setFont(font)
        self.tableWidget.setHorizontalHeaderItem(2, item)
        for index, kaf in enumerate(DataOddsTable.select()):
            self.tableWidget.setRowCount(index + 1)
            item = QtWidgets.QTableWidgetItem(f'{index + 1}')
            item.setFont(font)
            item.setToolTip(HELPING)
            self.tableWidget.setVerticalHeaderItem(index, item)
            name = QtWidgets.QTableWidgetItem(str(kaf.name))
            name.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.tableWidget.setItem(index, 0, name)
            cause = QtWidgets.QTableWidgetItem(str(kaf.cause))
            cause.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.tableWidget.setItem(index, 1, cause)
            value = QtWidgets.QTableWidgetItem(str(kaf.value))
            value.setTextAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            self.tableWidget.setItem(index, 2, value)
        self.tableWidget.resizeRowsToContents()
        self.tableWidget.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
        self.gridLayout_3.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(self.frame)
        self.frame_4.setMaximumSize(QtCore.QSize(697, 111))
        self.frame_4.setLayoutDirection(QtCore.Qt.RightToLeft)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.gridLayout_4 = QtWidgets.QGridLayout(self.frame_4)
        self.gridLayout_4.setObjectName("gridLayout_4")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(330, -1, -1, -1)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.cancel = QtWidgets.QPushButton(self.frame_4)
        self.cancel.setMaximumSize(QtCore.QSize(96, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.cancel.setFont(font)
        self.cancel.setObjectName("cancel")
        self.horizontalLayout.addWidget(self.cancel)
        self.add = QtWidgets.QPushButton(self.frame_4)
        self.add.setMaximumSize(QtCore.QSize(95, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.add.setFont(font)
        self.add.setObjectName("add")
        self.horizontalLayout.addWidget(self.add)
        self.enter = QtWidgets.QPushButton(self.frame_4)
        self.enter.setMaximumSize(QtCore.QSize(137, 28))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        self.enter.setFont(font)
        self.enter.setObjectName("enter")
        self.horizontalLayout.addWidget(self.enter)
        self.gridLayout_4.addLayout(self.horizontalLayout, 0, 0, 1, 1)
        self.verticalLayout.addWidget(self.frame_4)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 10)
        self.verticalLayout.setStretch(2, 2)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Окно выбора коэффициентов"))
        self.label.setText(_translate("MainWindow", "Список коэффициентов "))
        self.cancel.setText(_translate("MainWindow", "Отмена"))
        self.add.setText(_translate("MainWindow", "Добавить"))
        self.enter.setText(_translate("MainWindow", "Внести изменения"))
