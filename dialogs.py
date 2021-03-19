# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 19:13:20 2020

@author: stinc
"""
from PyQt5 import QtWidgets, uic, QtCore, QtGui
from design_enter_pipe import DnDialog
from design_enter_pump import PumpDialog
from models import MainPumpsTable, CoordinatesTable, SupportPumpsTable, PipeTable
from design_dialog_graph import GraphDialog
from design_save_dialog import SaveDialog
from settings import get_source_dict, update_dict_to_db
from design_dialog_delta import DialogDelta
from design_enter_diametre_pipe import PipeDnDialog
from design_dialog_choose_var import ChooseDialog
from design_window_add_pump import AddPumpDialog
from settings import get_list_main_pumps, get_list_sup_pumps, get_list_pipe
from design_window_add_sup_pump import AddSupPumpDialog
from design_window_add_pipe import AddPipeDialog
from design_window_choose_pipe import ChoosePipeDialog
from design_file_browser import Ui_MainWindow
from create_xls import CreatorXlsFile
from design_save_error_xls import ErrorXlsDialog
from design_dialog_error_enter_5 import ErrorDialogEnter5
from design_error_enter_number_data import ErrorEnterNumberDialog


class ErrorEnterNumberDialogWindow(QtWidgets.QDialog):
    def __init__(self):
        super(ErrorEnterNumberDialogWindow, self).__init__()
        self.ui = ErrorEnterNumberDialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.close)


class ChoosePipeDialogWindow(QtWidgets.QDialog):
    def __init__(self):
        super(ChoosePipeDialogWindow, self).__init__()
        self.ui = ChoosePipeDialog()
        self.ui.setupUi(self, PipeTable)
        self.ui.enter.clicked.connect(self.enter_pipe)
        self.ui.cancel_2.clicked.connect(self.close)
        self.ui.retry.clicked.connect(self.retry)
        self.list_indexes_column = [1, 2, 3]
        self.number = None

    def enter_pipe(self):
        self.number = self.ui.lineEdit.text()
        self.close()

    def get_number(self):
        return self.number

    def retry(self):
        self.ui.lineEdit.setText('')


class DnDialogWindow(QtWidgets.QDialog):
    def __init__(self, parent, var):
        super(DnDialogWindow, self).__init__(parent=parent)
        self.var = var
        self.ui = DnDialog()
        self.ui.setupUi(self, var)
        self.ui.enter.clicked.connect(self.enter)
        self.ui.retry.clicked.connect(self.retry)
        self.ui.cancel.clicked.connect(self.close)
        self.ui.choose.clicked.connect(self.choose_pipe)
        self.number = None

    def choose_pipe(self):
        self.choose_pipe_window = ChoosePipeDialogWindow()
        self.choose_pipe_window.exec()
        self.number = self.choose_pipe_window.get_number()
        if self.number is not None:
            list_characteristics = self.get_characteristics()
            self.ui.lineEdit.setText(str(list_characteristics[0]))
            self.ui.lineEdit_2.setText(str(list_characteristics[1]))

    def retry(self):
        self.ui.lineEdit.setText("")
        self.ui.lineEdit_2.setText("")
        self.ui.lineEdit_3.setText("")
        self.ui.lineEdit_4.setText("")
        self.ui.lineEdit_5.setText("")
        self.ui.lineEdit_6.setText("")

    def get_characteristics(self):
        info_pipe = PipeTable.get_or_none(PipeTable.id == self.number)
        return [info_pipe.R1n, info_pipe.k1]

    def enter(self):
        R1n = self.ui.lineEdit.text()
        k1 = self.ui.lineEdit_2.text()
        np = self.ui.lineEdit_3.text()
        kn = self.ui.lineEdit_4.text()
        k_a = self.ui.lineEdit_5.text()
        m = self.ui.lineEdit_6.text()
        list_with_value = [['R1n', R1n], ['k1', k1], ['np', np],
                           ['kn', kn], ['k_a', k_a], ['m_kaf', m]]
        dict_value = get_source_dict(self.var)
        for name, value in list_with_value:
            if type(value) == str and ',' in value:
                value = value.replace(',', '.')
            value = float(value)
            dict_value[name] = value
        update_dict_to_db(dict_value, self.var)
        self.close()


class PumpDialogWindow(QtWidgets.QDialog):
    def __init__(self, var, parent):
        super(PumpDialogWindow, self).__init__(parent=parent)
        self.var = var
        self.ui = PumpDialog()
        self.ui.setupUi(self, self.var)
        self.ui.next.clicked.connect(self.next)
        self.ui.enter.clicked.connect(self.enter)
        self.ui.retry.clicked.connect(self.retry)
        self.ui.cancel.clicked.connect(self.close)
        self.decision = None

    def next(self):
        self.decision = True
        self.close()

    def retry(self):
        self.ui.lineEdit.setText("")
        self.ui.lineEdit_2.setText("")
        self.ui.lineEdit_3.setText("")
        self.ui.lineEdit_4.setText("")
        self.ui.lineEdit_5.setText("")

    def get_decision(self):
        return self.decision

    def enter(self):
        brand_pump = self.ui.lineEdit.text()
        d_work = self.ui.lineEdit_2.text()
        Q_nom = self.ui.lineEdit_3.text()
        a = self.ui.lineEdit_4.text()
        b = self.ui.lineEdit_5.text()
        list_with_value = [['brand_pump_m', brand_pump], ['d_work_m', d_work], ['Q_nom_m', Q_nom],
                           ['a_m', a], ['b_m', b]]
        dict_value = get_source_dict(self.var)
        for name, value in list_with_value:
            if ',' in value:
                value = value.replace(',', '.')
            if name == 'Q_nom_m' or name == 'a_m' or name == 'b_m':
                value = float(value)
            dict_value[name] = value
        update_dict_to_db(dict_value, self.var)
        self.decision = True
        self.close()


class GraphDialogWindow(QtWidgets.QDialog):
    def __init__(self):
        super(GraphDialogWindow, self).__init__()
        self.ui = GraphDialog()
        self.ui.setupUi(self)
        self.ui.next.clicked.connect(self.close)
        self.ui.cancel.clicked.connect(self.cancel)

    def cancel(self):
        self.close()


class SaveDialogWindow(QtWidgets.QDialog):
    def __init__(self):
        super(SaveDialogWindow, self).__init__()
        self.ui = SaveDialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.save)
        self.ui.pushButton_2.clicked.connect(self.retry)
        self.name_var = None

    def save(self):
        self.name_var = self.ui.lineEdit.text()
        self.close()

    def return_name_var(self):
        return self.name_var

    def retry(self):
        self.ui.lineEdit.setText("")


class DialogDeltaWindow(QtWidgets.QDialog):
    def __init__(self):
        super(DialogDeltaWindow, self).__init__()
        self.ui = DialogDelta()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.close)


class DnDialogWindow_2(QtWidgets.QDialog):
    def __init__(self, parent, var):
        super(DnDialogWindow_2, self).__init__(parent=parent)
        self.var = var
        self.ui = PipeDnDialog()
        self.ui.setupUi(self, var)
        self.ui.next.clicked.connect(self.close)
        self.ui.retry.clicked.connect(self.retry)
        self.ui.enter.clicked.connect(self.enter)

    def retry(self):
        self.ui.lineEdit_7.setText("")

    def enter(self):
        Dn = self.ui.lineEdit_7.text()
        dict_value = get_source_dict(self.var)
        if type(Dn) == str and ',' in Dn:
            Dn = Dn.replace(',', '.')
        value = float(Dn)
        dict_value['Dn'] = value
        update_dict_to_db(dict_value, self.var)
        self.close()


class ChooseVarDialog(QtWidgets.QDialog):
    def __init__(self):
        super(ChooseVarDialog, self).__init__()
        self.ui = ChooseDialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.stay)
        self.ui.pushButton_2.clicked.connect(self.make_new_var)
        self.choosed_var = None

    def stay(self):
        self.choosed_var = True
        self.close()

    def make_new_var(self):
        self.choosed_var = False
        self.close()

    def get_decision(self):
        return self.choosed_var


class AddPumpDialogWindow(QtWidgets.QDialog):
    def __init__(self):
        super(AddPumpDialogWindow, self).__init__()
        self.ui = AddPumpDialog()
        self.ui.setupUi(self, MainPumpsTable)
        self.ui.enter.clicked.connect(self.enter_pump)
        self.ui.cancel.clicked.connect(self.close)
        self.ui.retry.clicked.connect(self.retry)
        self.ui.add.clicked.connect(self.add_row)
        self.index_tableWidget_pump_enter_2 = 1
        self.list_indexes_column = [3, 4, 5, 6]

    def add_row(self):
        self.index_tableWidget_pump_enter_2 += 1
        self.ui.tableWidget_pump_enter_2.setRowCount(self.index_tableWidget_pump_enter_2)

    def enter_pump(self):
        list_main_pumps_from_bd = get_list_main_pumps()
        checker = False
        for i in range(self.ui.tableWidget_pump_enter_2.rowCount()):
            list_checked_value = []
            for index in range(self.ui.tableWidget_pump_enter_2.columnCount()):
                value_object = self.ui.tableWidget_pump_enter_2.item(i, index)
                if value_object is None:
                    checker = True
                    break
                value = value_object.text()
                if index in self.list_indexes_column:
                    if type(value) == str and ',' in value:
                        value = value.replace(',', '.')
                    value_float = float(value)
                    list_checked_value.append(value_float)
                else:
                    list_checked_value.append(value)
            if checker:
                break
            list_main_pumps_from_bd.append(list_checked_value)
        list_main_pumps_from_bd.sort(key=lambda k: k[5])
        source = MainPumpsTable.delete()
        source.execute()
        for brand, rotor, impeller_diameter, a, b, Q_nom, kaf in list_main_pumps_from_bd:
            main_pump = MainPumpsTable(
                brand=brand,
                rotor=rotor,
                impeller_diameter=impeller_diameter,
                a=a,
                b=b,
                Q_nom=Q_nom,
                kaf=kaf
            )
            main_pump.save()
        self.ui.enter_data_from_db(MainPumpsTable)

    def retry(self):
        self.index_tableWidget_pump_enter_2 = 0
        self.ui.tableWidget_pump_enter_2.setRowCount(self.index_tableWidget_pump_enter_2)


class AddSupPumpDialogWindow(QtWidgets.QDialog):
    def __init__(self):
        super(AddSupPumpDialogWindow, self).__init__()
        self.ui = AddSupPumpDialog()
        self.ui.setupUi(self, SupportPumpsTable)
        self.ui.enter.clicked.connect(self.enter_pump)
        self.ui.cancel_2.clicked.connect(self.close)
        self.ui.retry.clicked.connect(self.retry)
        self.ui.add.clicked.connect(self.add_row)
        self.index_tableWidget = 1
        self.list_indexes_column = [2, 3, 4]

    def add_row(self):
        self.index_tableWidget += 1
        self.ui.tableWidget.setRowCount(self.index_tableWidget)

    def enter_pump(self):
        list_sup_pumps_from_bd = get_list_sup_pumps()
        checker = False
        for i in range(self.ui.tableWidget.rowCount()):
            list_checked_value = []
            for index in range(self.ui.tableWidget.columnCount()):
                value_object = self.ui.tableWidget.item(i, index)
                if value_object is None:
                    checker = True
                    break
                value = value_object.text()
                if index in self.list_indexes_column:
                    if type(value) == str and ',' in value:
                        value = value.replace(',', '.')
                    value_float = float(value)
                    list_checked_value.append(value_float)
                else:
                    list_checked_value.append(value)
            if checker:
                break
            list_sup_pumps_from_bd.append(list_checked_value)
        list_sup_pumps_from_bd.sort(key=lambda k: k[4])
        source = SupportPumpsTable.delete()
        source.execute()
        for brand, impeller_diameter, a, b, Q_nom in list_sup_pumps_from_bd:
            sup_pump = SupportPumpsTable(
                brand=brand,
                impeller_diameter=impeller_diameter,
                a=a,
                b=b,
                Q_nom=Q_nom,
            )
            sup_pump.save()
        self.ui.enter_table_data(SupportPumpsTable)

    def retry(self):
        self.index_tableWidget = 0
        self.ui.tableWidget.setRowCount(self.index_tableWidget)


class AddPipeDialogWindow(QtWidgets.QDialog):
    def __init__(self):
        super(AddPipeDialogWindow, self).__init__()
        self.ui = AddPipeDialog()
        self.ui.setupUi(self, PipeTable)
        self.ui.enter.clicked.connect(self.enter_pipe)
        self.ui.cancel_2.clicked.connect(self.close)
        self.ui.retry.clicked.connect(self.retry)
        self.ui.add.clicked.connect(self.add_row)
        self.index_tableWidget_pipe_enter_2 = 1
        self.list_indexes_column = [1, 2, 3]

    def add_row(self):
        self.index_tableWidget_pipe_enter_2 += 1
        self.ui.tableWidget_pipe_enter_2.setRowCount(self.index_tableWidget_pipe_enter_2)

    def enter_pipe(self):
        list_pipes_from_bd = get_list_pipe()
        checker = False
        for i in range(self.ui.tableWidget_pipe_enter_2.rowCount()):
            list_checked_value = []
            for index in range(self.ui.tableWidget_pipe_enter_2.columnCount()):
                value_object = self.ui.tableWidget_pipe_enter_2.item(i, index)
                if value_object is None:
                    checker = True
                    break
                value = value_object.text()
                if index in self.list_indexes_column:
                    if type(value) == str and ',' in value:
                        value = value.replace(',', '.')
                    value_float = float(value)
                    list_checked_value.append(value_float)
                else:
                    list_checked_value.append(value)
            if checker:
                break
            list_pipes_from_bd.append(list_checked_value)
        list_pipes_from_bd.sort(key=lambda k: k[1])
        source = PipeTable.delete()
        source.execute()
        for brand, diameter, R1n, k1 in list_pipes_from_bd:
            pipe = PipeTable(
                brand=brand,
                diameter=diameter,
                R1n=R1n,
                k1=k1
            )
            pipe.save()
        self.ui.enter_data_table(PipeTable)

    def retry(self):
        self.index_tableWidget_pipe_enter_2 = 0
        self.ui.tableWidget_pipe_enter_2.setRowCount(self.index_tableWidget_pipe_enter_2)


class ErrorXlsDialogWindow(QtWidgets.QDialog):
    def __init__(self):
        super(ErrorXlsDialogWindow, self).__init__()
        self.ui = ErrorXlsDialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.close)


class ErrorDialogEnter5Window(QtWidgets.QDialog):
    def __init__(self):
        super(ErrorDialogEnter5Window, self).__init__()
        self.ui = ErrorDialogEnter5()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.close)


class MyFileBrowser(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, var):
        super(MyFileBrowser, self).__init__()
        self.setupUi(self)
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.context_menu)
        self.populate()
        self.cancel_2.clicked.connect(self.close)
        self.save_2.clicked.connect(self.save_data_xls)
        self.file_type = False
        self.lineEdit_2.setText('C:/')
        self.var = var

    def save_data_xls(self):
        if self.file_type is True:
            self.error_xls_window = ErrorXlsDialogWindow()
            self.error_xls_window.exec()
            return
        file_name = self.lineEdit.text()
        if file_name == '':
            file_name = self.var
        if ' ' in file_name:
            file_name = file_name.replace(' ', '_')
        file_path = self.lineEdit_2.text()
        file_name += '.xls'
        creator_xls_file = CreatorXlsFile(file_path, file_name, self.var)
        creator_xls_file.save()
        self.close()

    def populate(self):
        self.model = QtWidgets.QFileSystemModel()
        self.model.setRootPath((QtCore.QDir.rootPath()))
        self.treeView.setModel(self.model)
        self.treeView.setSortingEnabled(True)

    def context_menu(self):
        menu = QtWidgets.QMenu()
        open = menu.addAction('Выбрать')
        open.triggered.connect(self.open_file)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def open_file(self):
        index = self.treeView.currentIndex()
        self.file_path = self.model.filePath(index)
        self.file_type = self.model.fileInfo(index).isFile()
        self.lineEdit_2.setText(self.file_path)
