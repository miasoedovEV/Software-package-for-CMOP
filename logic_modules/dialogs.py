# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 19:13:20 2020

@author: stinc
"""
from PyQt5 import QtWidgets, QtCore, QtGui
from design.design_enter_pipe import DnDialog
from design.design_enter_pump import PumpDialog
from design.design_error_number_list import ErrorListNumberDialog
from database.models import MainPumpsTable, SupportPumpsTable, PipeTable, DataOddsTable
from design.design_dialog_graph import GraphDialog
from design.design_save_dialog import SaveDialog
from logic_modules.settings import get_source_dict, update_dict_to_db, check_data, get_list_main_pumps, \
    get_list_sup_pumps, get_list_pipe
from design.design_dialog_delta import DialogDelta
from design.design_enter_diametre_pipe import PipeDnDialog
from design.design_dialog_choose_var import ChooseDialog
from design.design_window_add_pump import AddPumpDialog
from design.design_window_add_sup_pump import AddSupPumpDialog
from design.design_window_add_pipe import AddPipeDialog
from design.design_window_choose_pipe import ChoosePipeDialog
from design.design_file_browser import Ui_MainWindow
from logic_modules.create_xls import CreatorXlsFile
from design.design_save_error_xls import ErrorXlsDialog
from design.design_dialog_error_enter_5 import ErrorDialogEnter5
from design.design_error_enter_number_data import ErrorEnterNumberDialog
from design.design_window_error_saving import ErrorSaveDialog
from design.design_error_export_xsl import ErrorExportDialog
from design.designer_window_list_kaf import WindowKafList
from design.design_help_window import HelpDialog

HELPING = 'Кликните правой кнопкой кнопкой мыши по строчке, которую хотите удалить.'
HELPING_FOR_KAF = 'Кликните правой кнопкой кнопкой мыши по строчке коэффициента, который хотите выбрать. '
ICON = 'support_files\\2truba.ico'


class CopySelectedCellsAction(QtWidgets.QAction):
    def __init__(self, list_table_widget):
        super(CopySelectedCellsAction, self).__init__()
        self.setShortcut('Ctrl+C')
        self.list_table_widget = list_table_widget
        self.triggered.connect(self.copy_cells_to_clipboard)

    def copy_cells_to_clipboard(self):
        for table in self.list_table_widget:
            if len(table.selectionModel().selectedIndexes()) < 1:
                continue
                # sort select indexes into rows and columns
            previous = table.selectionModel().selectedIndexes()[0]
            columns = []
            rows = []
            for index in table.selectionModel().selectedIndexes():
                if previous.column() != index.column():
                    columns.append(rows)
                    rows = []
                rows.append(index.data())
                previous = index
            columns.append(rows)
            # add rows and columns to clipboard
            clipboard = ""
            nrows = len(columns[0])
            ncols = len(columns)
            for r in range(nrows):
                for c in range(ncols):
                    if columns[c][r] is None:
                        continue
                    clipboard += columns[c][r]
                    if c != (ncols - 1):
                        clipboard += '\t'
                clipboard += '\n'
            # copy to the system clipboard
            sys_clip = QtWidgets.QApplication.clipboard()
            sys_clip.setText(clipboard)
            table.clearSelection()


class PastSelectedCellsAction(QtWidgets.QAction):
    def __init__(self, list_table_widget):
        super(PastSelectedCellsAction, self).__init__()
        self.setShortcut('Ctrl+V')
        self.list_table_widget = list_table_widget
        self.triggered.connect(self.past_cells_to_clipboard)

    def past_cells_to_clipboard(self):
        sys_clip = QtWidgets.QApplication.clipboard()
        text = sys_clip.text()
        elements = text.split('\n')
        for table in self.list_table_widget:
            if len(table.selectionModel().selectedIndexes()) < 1:
                continue
            for index, index_table in enumerate(table.selectionModel().selectedIndexes()):
                if len(elements) < index + 1:
                    return
                item = QtWidgets.QTableWidgetItem(elements[index])
                table.setItem(index_table.row(), index_table.column(), item)
                table.clearSelection()


def check_value_None(value):
    if value == '' or value is None:
        error_dialog_enter = ErrorDialogEnterWindow()
        error_dialog_enter.exec()
        return None
    else:
        return True


def check_value_number(value):
    if check_data(value) is None:
        error_enter_Number = ErrorEnterNumberDialogWindow()
        error_enter_Number.exec()
        return None
    else:
        return True


def delete_string_from_db(db, index):
    source = db.delete().where(db.id == index + 1)
    source.execute()


class ErrorExportDialogWindow(QtWidgets.QDialog):
    def __init__(self):
        super(ErrorExportDialogWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon(ICON))
        self.ui = ErrorExportDialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.close)


class ErrorSaveDialogWindow(QtWidgets.QDialog):
    def __init__(self):
        super(ErrorSaveDialogWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon(ICON))
        self.ui = ErrorSaveDialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.close)


class ErrorEnterNumberDialogWindow(QtWidgets.QDialog):
    def __init__(self):
        super(ErrorEnterNumberDialogWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon(ICON))
        self.ui = ErrorEnterNumberDialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.close)


class ErrorListNumberDialogWindow(QtWidgets.QDialog):
    def __init__(self):
        super(ErrorListNumberDialogWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon(ICON))
        self.ui = ErrorListNumberDialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.close)


class ChoosePipeDialogWindow(QtWidgets.QDialog):
    def __init__(self, R1, k1):
        super(ChoosePipeDialogWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon(ICON))
        self.ui = ChoosePipeDialog()
        self.ui.setupUi(self, PipeTable)
        self.ui.enter.clicked.connect(self.enter_pipe)
        self.ui.cancel_2.clicked.connect(self.close)
        self.ui.retry.clicked.connect(self.retry)
        self.information_pipe = None
        self.ui.tableWidget_pipe.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.tableWidget_pipe.customContextMenuRequested.connect(self.context_menu)
        self.R1 = R1
        self.k1 = k1

    def enter_pipe(self):
        self.number = self.ui.lineEdit.text()
        if check_value_None(self.number) is None:
            return
        if check_value_number(self.number) is None:
            return
        info_pipe = PipeTable.get_or_none(PipeTable.id == self.number)
        if info_pipe is None:
            self.error_list_number_window = ErrorListNumberDialogWindow()
            self.error_list_number_window.exec()
            return
        self.information_pipe = [info_pipe.R1n, info_pipe.k1]
        self.close()

    def get_number(self):
        return self.information_pipe

    def retry(self):
        self.ui.lineEdit.clear()

    def context_menu(self):
        menu = QtWidgets.QMenu()
        open = menu.addAction('Выбрать')
        open.triggered.connect(self.choose_pipe)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def choose_pipe(self):
        index = self.ui.tableWidget_pipe.currentIndex()
        if index.row() == -1:
            return
        R1_from_table = self.ui.tableWidget_pipe.item(index.row(), 2).text()
        k1_from_table = self.ui.tableWidget_pipe.item(index.row(), 3).text()
        self.R1.setText(R1_from_table)
        self.k1.setText(k1_from_table)


class WindowChooseKaf(QtWidgets.QMainWindow):
    def __init__(self, parent, np, kn, m, help):
        super(WindowChooseKaf, self).__init__(parent=parent)
        self.setWindowIcon(QtGui.QIcon(ICON))
        self.ui = WindowKafList()
        self.ui.setupUi(self, DataOddsTable, help)
        self.ui.cancel.clicked.connect(self.close)
        self.ui.add.clicked.connect(self.add_row_list)
        self.ui.tableWidget.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.tableWidget.customContextMenuRequested.connect(self.context_menu)
        self.np = np
        self.kn = kn
        self.m = m
        self.ui.enter.clicked.connect(self.update_table_kaf)
        self.add_copy_past_actions()

    def add_row_list(self):
        index_table_widget = self.ui.tableWidget.rowCount() + 1
        self.ui.tableWidget.setRowCount(index_table_widget)
        item = QtWidgets.QTableWidgetItem(f'{index_table_widget}')
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        item.setFont(font)
        self.ui.tableWidget.setVerticalHeaderItem(index_table_widget - 1, item)

    def context_menu(self):
        menu = QtWidgets.QMenu()
        open = menu.addAction('Выбрать')
        open.triggered.connect(self.enter_kaf)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def enter_kaf(self):
        index = self.ui.tableWidget.currentIndex()
        if index.row() == -1:
            return
        self.value = self.ui.tableWidget.item(index.row(), 2).text()
        self.name = self.ui.tableWidget.item(index.row(), 0).text()
        if self.name == 'np':
            self.np.setText(self.value)
        elif self.name == 'kн':
            self.kn.setText(self.value)
        elif self.name == 'm':
            self.m.setText(self.value)

    def update_table_kaf(self):
        source = DataOddsTable.delete()
        source.execute()
        for i in range(self.ui.tableWidget.rowCount()):
            name_object = self.ui.tableWidget.item(i, 0)
            cause_object = self.ui.tableWidget.item(i, 1)
            value_object = self.ui.tableWidget.item(i, 2)
            name = self.check_value(name_object)
            cause = self.check_value(cause_object)
            value = self.check_value(value_object)
            if name is None or cause is None or value is None:
                continue
            if check_value_number(value) is None:
                continue
            data = DataOddsTable(
                name=name,
                cause=cause,
                value=value
            )
            data.save()

    def check_value(self, value_object):
        if value_object is None:
            return None
        value = value_object.text()
        if value == '':
            return None
        return value

    def check_number(self, value):
        if check_data(value) is None:
            self.show_error_enter_number()
            return None
        else:
            return value

    def show_error_enter(self):
        self.error_dialog_enter_5 = ErrorDialogEnterWindow()
        self.error_dialog_enter_5.exec()

    def show_error_enter_number(self):
        self.error_enter_Number = ErrorEnterNumberDialogWindow()
        self.error_enter_Number.exec()

    def add_copy_past_actions(self):
        list_table = [self.ui.tableWidget]
        self.copy_action = CopySelectedCellsAction(list_table)
        self.past_action = PastSelectedCellsAction(list_table)
        self.addAction(self.copy_action)
        self.addAction(self.past_action)


class DnDialogWindow(QtWidgets.QDialog):
    def __init__(self, parent, var):
        super(DnDialogWindow, self).__init__(parent=parent)
        self.setWindowIcon(QtGui.QIcon(ICON))
        self.var = var
        self.ui = DnDialog()
        self.ui.setupUi(self, var)
        self.ui.enter.clicked.connect(self.enter)
        self.ui.retry.clicked.connect(self.retry)
        self.ui.cancel.clicked.connect(self.close)
        self.ui.choose.clicked.connect(self.choose_pipe)
        self.ui.choose_k.clicked.connect(self.choose_kaf)
        self.information_pipe = None
        self.decision = None

    def choose_kaf(self):
        self.windpw_list_kaf = WindowChooseKaf(self, np=self.ui.lineEdit_3, kn=self.ui.lineEdit_4,
                                               m=self.ui.lineEdit_6, help=HELPING_FOR_KAF)
        self.windpw_list_kaf.show()

    def choose_pipe(self):
        self.choose_pipe_window = ChoosePipeDialogWindow(self.ui.lineEdit, self.ui.lineEdit_2)
        self.choose_pipe_window.exec()
        self.information_pipe = self.choose_pipe_window.get_number()
        if self.information_pipe is not None:
            self.ui.lineEdit.setText(str(self.information_pipe[0]))
            self.ui.lineEdit_2.setText(str(self.information_pipe[1]))

    def retry(self):
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()
        self.ui.lineEdit_5.clear()
        self.ui.lineEdit_6.clear()

    def enter(self):
        R1n = self.ui.lineEdit.text()
        k1 = self.ui.lineEdit_2.text()
        np = self.ui.lineEdit_3.text()
        kn = self.ui.lineEdit_4.text()
        k_a = self.ui.lineEdit_5.text()
        m = self.ui.lineEdit_6.text()
        list_with_value = [['R1n', R1n], ['k1', k1], ['np', np],
                           ['kn', kn], ['k_a', k_a], ['m_kaf', m]]
        for value in list_with_value:
            if check_value_None(value[1]) is None:
                return
            if check_value_number(value[1]) is None:
                return
        dict_value = get_source_dict(self.var)
        for name, value in list_with_value:
            if type(value) == str and ',' in value:
                value = value.replace(',', '.')
            value = float(value)
            dict_value[name] = value
        update_dict_to_db(dict_value, self.var)
        self.decision = True
        self.close()

    def get_decision(self):
        return self.decision


class PumpDialogWindow(QtWidgets.QDialog):
    def __init__(self, var, parent):
        super(PumpDialogWindow, self).__init__(parent=parent)
        self.setWindowIcon(QtGui.QIcon(ICON))
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
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.lineEdit_3.clear()
        self.ui.lineEdit_4.clear()
        self.ui.lineEdit_5.clear()

    def get_decision(self):
        return self.decision

    def enter(self):
        brand_pump = self.ui.lineEdit.text()
        d_work = self.ui.lineEdit_2.text()
        Q_nom = self.ui.lineEdit_3.text()
        a = self.ui.lineEdit_4.text()
        b = self.ui.lineEdit_5.text()
        list_values = [brand_pump, d_work, Q_nom, a, b]
        for index, value in enumerate(list_values):
            if check_value_None(value) is None:
                return
            if index == 0:
                continue
            if check_value_number(value) is None:
                return
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
        self.setWindowIcon(QtGui.QIcon(ICON))
        self.ui = GraphDialog()
        self.ui.setupUi(self)
        self.ui.next.clicked.connect(self.close)
        self.ui.cancel.clicked.connect(self.cancel)

    def cancel(self):
        self.close()


class SaveDialogWindow(QtWidgets.QDialog):
    def __init__(self):
        super(SaveDialogWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon(ICON))
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
        self.ui.lineEdit.clear()


class DialogDeltaWindow(QtWidgets.QDialog):
    def __init__(self):
        super(DialogDeltaWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon(ICON))
        self.ui = DialogDelta()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.close)


class DnDialogWindow_2(QtWidgets.QDialog):
    def __init__(self, parent, var):
        super(DnDialogWindow_2, self).__init__(parent=parent)
        self.setWindowIcon(QtGui.QIcon(ICON))
        self.var = var
        self.ui = PipeDnDialog()
        self.ui.setupUi(self, var)
        self.ui.next.clicked.connect(self.next)
        self.ui.retry.clicked.connect(self.retry)
        self.ui.enter.clicked.connect(self.enter)
        self.decision = None

    def next(self):
        self.decision = True
        self.close()

    def retry(self):
        self.ui.lineEdit_7.clear()

    def enter(self):
        Dn = self.ui.lineEdit_7.text()
        if check_value_None(Dn) is None:
            return
        if check_value_number(Dn) is None:
            return
        dict_value = get_source_dict(self.var)
        if type(Dn) == str and ',' in Dn:
            Dn = Dn.replace(',', '.')
        value = float(Dn)
        dict_value['Dn'] = value
        update_dict_to_db(dict_value, self.var)
        self.decision = True
        self.close()

    def get_decision(self):
        return self.decision


class ChooseVarDialog(QtWidgets.QDialog):
    def __init__(self):
        super(ChooseVarDialog, self).__init__()
        self.setWindowIcon(QtGui.QIcon(ICON))
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
        self.setWindowIcon(QtGui.QIcon(ICON))
        self.ui = AddPumpDialog()
        self.ui.setupUi(self, MainPumpsTable, HELPING)
        self.ui.enter.clicked.connect(self.enter_pump)
        self.ui.cancel.clicked.connect(self.close)
        self.ui.retry.clicked.connect(self.retry)
        self.ui.add.clicked.connect(self.add_row)
        self.list_indexes_column = [3, 4, 5, 6]
        self.ui.tableWidget_pump_enter.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.tableWidget_pump_enter.customContextMenuRequested.connect(self.context_menu)
        self.add_copy_past_actions()

    def add_row(self):
        index_tableWidget_pump_enter_2 = self.ui.tableWidget_pump_enter_2.rowCount() + 1
        self.ui.tableWidget_pump_enter_2.setRowCount(index_tableWidget_pump_enter_2)
        item = QtWidgets.QTableWidgetItem(f'{index_tableWidget_pump_enter_2}')
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        item.setFont(font)
        self.ui.tableWidget_pump_enter_2.setVerticalHeaderItem(index_tableWidget_pump_enter_2 - 1, item)

    def enter_pump(self):
        list_main_pumps_from_bd = get_list_main_pumps()
        checker = False
        for i in range(self.ui.tableWidget_pump_enter_2.rowCount()):
            list_checked_value = []
            for index in range(self.ui.tableWidget_pump_enter_2.columnCount()):
                value_object = self.ui.tableWidget_pump_enter_2.item(i, index)
                if i > 0:
                    if value_object is None:
                        checker = True
                        break
                if check_value_None(value_object) is None:
                    return
                value = value_object.text()
                if index in self.list_indexes_column:
                    if check_value_number(value) is None:
                        return
                    if type(value) == str and ',' in value:
                        value = value.replace(',', '.')
                    value_float = float(value)
                    list_checked_value.append(value_float)
                else:
                    list_checked_value.append(value)
            if checker:
                break
            if len(list_checked_value) != self.ui.tableWidget_pump_enter_2.columnCount():
                self.error_dialog_enter = ErrorDialogEnterWindow()
                self.error_dialog_enter.exec()
                return
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
        self.ui.enter_data_from_db(MainPumpsTable, HELPING)

    def retry(self):
        self.index_tableWidget_pump_enter_2 = 0
        self.ui.tableWidget_pump_enter_2.setRowCount(self.index_tableWidget_pump_enter_2)

    def context_menu(self):
        menu = QtWidgets.QMenu()
        open = menu.addAction('Удалить')
        open.triggered.connect(self.delete_pump)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def delete_pump(self):
        index = self.ui.tableWidget_pump_enter.currentIndex()
        if index.row() == -1:
            return
        delete_string_from_db(MainPumpsTable, index.row())
        self.ui.tableWidget_pump_enter.removeRow(index.row())

    def add_copy_past_actions(self):
        list_table = [self.ui.tableWidget_pump_enter, self.ui.tableWidget_pump_enter_2]
        self.copy_action = CopySelectedCellsAction(list_table)
        self.past_action = PastSelectedCellsAction(list_table)
        self.addAction(self.copy_action)
        self.addAction(self.past_action)


class AddSupPumpDialogWindow(QtWidgets.QDialog):
    def __init__(self):
        super(AddSupPumpDialogWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon(ICON))
        self.ui = AddSupPumpDialog()
        self.ui.setupUi(self, SupportPumpsTable, HELPING)
        self.ui.enter.clicked.connect(self.enter_pump)
        self.ui.cancel_2.clicked.connect(self.close)
        self.ui.retry.clicked.connect(self.retry)
        self.ui.add.clicked.connect(self.add_row)
        self.list_indexes_column = [2, 3, 4]
        self.ui.tableWidget_pump_enter.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.tableWidget_pump_enter.customContextMenuRequested.connect(self.context_menu)
        self.add_copy_past_actions()

    def add_row(self):
        index_tableWidget = self.ui.tableWidget.rowCount() + 1
        self.ui.tableWidget.setRowCount(index_tableWidget)
        item = QtWidgets.QTableWidgetItem(f'{index_tableWidget}')
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        item.setFont(font)
        self.ui.tableWidget.setVerticalHeaderItem(index_tableWidget - 1, item)

    def enter_pump(self):
        list_sup_pumps_from_bd = get_list_sup_pumps()
        checker = False
        for i in range(self.ui.tableWidget.rowCount()):
            list_checked_value = []
            for index in range(self.ui.tableWidget.columnCount()):
                value_object = self.ui.tableWidget.item(i, index)
                if i > 0:
                    if value_object is None:
                        checker = True
                        break
                if check_value_None(value_object) is None:
                    return
                value = value_object.text()
                if index in self.list_indexes_column:
                    if check_value_number(value) is None:
                        return
                    if type(value) == str and ',' in value:
                        value = value.replace(',', '.')
                    value_float = float(value)
                    list_checked_value.append(value_float)
                else:
                    list_checked_value.append(value)
            if checker:
                break
            if len(list_checked_value) != self.ui.tableWidget.columnCount():
                self.error_dialog_enter = ErrorDialogEnterWindow()
                self.error_dialog_enter.exec()
                return
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
        self.ui.enter_table_data(SupportPumpsTable, HELPING)

    def retry(self):
        self.index_tableWidget = 0
        self.ui.tableWidget.setRowCount(self.index_tableWidget)

    def context_menu(self):
        menu = QtWidgets.QMenu()
        open = menu.addAction('Удалить')
        open.triggered.connect(self.delete_sup_pump)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def delete_sup_pump(self):
        index = self.ui.tableWidget_pump_enter.currentIndex()
        if index.row() == -1:
            return
        delete_string_from_db(SupportPumpsTable, index.row())
        self.ui.tableWidget_pump_enter.removeRow(index.row())

    def add_copy_past_actions(self):
        list_table = [self.ui.tableWidget, self.ui.tableWidget_pump_enter]
        self.copy_action = CopySelectedCellsAction(list_table)
        self.past_action = PastSelectedCellsAction(list_table)
        self.addAction(self.copy_action)
        self.addAction(self.past_action)


class AddPipeDialogWindow(QtWidgets.QDialog):
    def __init__(self):
        super(AddPipeDialogWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon(ICON))
        self.ui = AddPipeDialog()
        self.ui.setupUi(self, PipeTable, HELPING)
        self.ui.enter.clicked.connect(self.enter_pipe)
        self.ui.cancel_2.clicked.connect(self.close)
        self.ui.retry.clicked.connect(self.retry)
        self.ui.add.clicked.connect(self.add_row)
        self.list_indexes_column = [1, 2, 3]
        self.ui.tableWidget_pipe.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.tableWidget_pipe.customContextMenuRequested.connect(self.context_menu)
        self.add_copy_past_actions()

    def add_row(self):
        index_tableWidget_pipe_enter_2 = self.ui.tableWidget_pipe_enter_2.rowCount() + 1
        self.ui.tableWidget_pipe_enter_2.setRowCount(index_tableWidget_pipe_enter_2)
        item = QtWidgets.QTableWidgetItem(f'{index_tableWidget_pipe_enter_2}')
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        item.setFont(font)
        self.ui.tableWidget_pipe_enter_2.setVerticalHeaderItem(index_tableWidget_pipe_enter_2 - 1, item)

    def enter_pipe(self):
        list_pipes_from_bd = get_list_pipe()
        checker = False
        for i in range(self.ui.tableWidget_pipe_enter_2.rowCount()):
            list_checked_value = []
            for index in range(self.ui.tableWidget_pipe_enter_2.columnCount()):
                value_object = self.ui.tableWidget_pipe_enter_2.item(i, index)
                if i > 0:
                    if value_object is None:
                        checker = True
                        break
                if check_value_None(value_object) is None:
                    return
                value = value_object.text()
                if index in self.list_indexes_column:
                    if check_value_number(value) is None:
                        return
                    if type(value) == str and ',' in value:
                        value = value.replace(',', '.')
                    value_float = float(value)
                    list_checked_value.append(value_float)
                else:
                    list_checked_value.append(value)
            if checker:
                break
            if len(list_checked_value) != self.ui.tableWidget_pipe_enter_2.columnCount():
                self.error_dialog_enter = ErrorDialogEnterWindow()
                self.error_dialog_enter.exec()
                return
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
        self.ui.enter_data_table(PipeTable, HELPING)

    def retry(self):
        self.index_tableWidget_pipe_enter_2 = 0
        self.ui.tableWidget_pipe_enter_2.setRowCount(self.index_tableWidget_pipe_enter_2)

    def context_menu(self):
        menu = QtWidgets.QMenu()
        open = menu.addAction('Удалить')
        open.triggered.connect(self.delete_pipe)
        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    def delete_pipe(self):
        index = self.ui.tableWidget_pipe.currentIndex()
        if index.row() == -1:
            return
        delete_string_from_db(PipeTable, index.row())
        self.ui.tableWidget_pipe.removeRow(index.row())

    def add_copy_past_actions(self):
        list_table = [self.ui.tableWidget_pipe, self.ui.tableWidget_pipe_enter_2]
        self.copy_action = CopySelectedCellsAction(list_table)
        self.past_action = PastSelectedCellsAction(list_table)
        self.addAction(self.copy_action)
        self.addAction(self.past_action)


class ErrorXlsDialogWindow(QtWidgets.QDialog):
    def __init__(self):
        super(ErrorXlsDialogWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon(ICON))
        self.ui = ErrorXlsDialog()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.close)


class ErrorDialogEnterWindow(QtWidgets.QDialog):
    def __init__(self):
        super(ErrorDialogEnterWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon(ICON))
        self.ui = ErrorDialogEnter5()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.close)


class MyFileBrowser(Ui_MainWindow, QtWidgets.QMainWindow):
    def __init__(self, var):
        super(MyFileBrowser, self).__init__()
        self.setWindowIcon(QtGui.QIcon(ICON))
        self.setupUi(self)
        self.treeView.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.treeView.customContextMenuRequested.connect(self.context_menu)
        self.populate()
        self.cancel_2.clicked.connect(self.close)
        self.save_2.clicked.connect(self.save_data_xls)
        self.file_type = False
        self.var = var

    def save_data_xls(self):
        if self.file_type is True:
            self.error_xls_window = ErrorXlsDialogWindow()
            self.error_xls_window.exec()
            return
        if self.lineEdit_2.text() is None or self.lineEdit_2.text() == '':
            return
        file_name = self.lineEdit.text()
        if file_name == '':
            file_name = self.var
        if ' ' in file_name:
            file_name = file_name.replace(' ', '_')
        file_name += '.xls'
        file_path = self.lineEdit_2.text()
        creator_xls_file = CreatorXlsFile(file_path, file_name, self.var)
        try:
            creator_xls_file.save()
        except PermissionError:
            self.error_export_window = ErrorExportDialogWindow()
            self.error_export_window.exec()
        else:
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


class HelpDialogWindow(HelpDialog, QtWidgets.QMainWindow):
    def __init__(self):
        super(HelpDialogWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon(ICON))
        self.setupUi(self)
