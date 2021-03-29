# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 19:13:20 2020

@author: stinc
"""
import time
import breeze_resources
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import QThread, QFile, QTextStream
from dialogs import DnDialogWindow, PumpDialogWindow, GraphDialogWindow, SaveDialogWindow, DialogDeltaWindow, \
    DnDialogWindow_2, ChooseVarDialog, AddPumpDialogWindow, AddSupPumpDialogWindow, AddPipeDialogWindow, MyFileBrowser, \
    ErrorDialogEnterWindow, ErrorEnterNumberDialogWindow, ErrorSaveDialogWindow
from models import MainPumpsTable, CoordinatesTable, SourceDataTable, ActionVarTable
import json
from calculate_5_class import Calculate5, draw_graph_in_calculate
from draw_graph import drawing_autocad, drawing_plt
from calculate_7_class import Calculate7, LIST_WITH_NAME_DATA_TABLE7, MODE_CALCULATE_7
from settings import get_source_dict, update_dict_to_db, check_update_data_var_7, get_info_table_list, get_table_list_8, \
    update_list_coordinates_to_db, create_new_data_var_5, delete_data_7_8, check_list_late_source_data_8, delete_func, \
    load_update_var_state, get_state_var, update_var_table, LIST_WITH_NAME_VALUE_CHARACTIRISTIES, \
    LIST_WITH_NAME_VALUE_OIL_PROPERTIES, LIST_WITH_VALUE, LIST_WITH_NAME, FIRST_NAME_ACTION_VAR, FIRST_NAME_VAR, \
    LIST_WITH_TABLE_VALUE_CALC_7, LIST_WITH_NAME_SOURCE_VALUE_8, check_data, NUMBER_LOW_INDEX
from calculate_8_class import CalculationModesNps
from tab_ui import MyWindow


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


class External(QThread):

    def __init__(self, main_window):
        super().__init__()
        self.main_window = main_window
        self.list_func = [self.main_window.calculator_5.calculate_third_part,
                          self.main_window.calculator_5.calculate_fourth_part,
                          load_update_var_state,
                          self.main_window.insert_values]

    def run(self):
        self.main_window.ui.frame_25.show()
        value = 0
        for index, func in enumerate(self.list_func):
            if index == 2:
                func(self.main_window.var, 1)
                time.sleep(1)
                value += 25
            elif index == 3:
                func(self.main_window.var)
                time.sleep(1)
                value += 24
            else:
                func()
                value += 25
            self.main_window.ui.progressBar.setValue(value)
        else:
            self.main_window.ui.progressBar.setValue(0)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setWindowIcon(QtGui.QIcon('2truba.ico'))
        self.ui = MyWindow()
        self.ui.setupUi(self, MainPumpsTable)
        self.ui.pushButton_1.clicked.connect(self.calculate_5)
        self.ui.pushButton_2.clicked.connect(self.erase_data)
        self.ui.shower.clicked.connect(self.show_graphs)
        self.ui.shower.setVisible(False)
        self.ui.pushButton_3.clicked.connect(self.make_func_add_line_table(self.ui.table))
        self.ui.Add_2.clicked.connect(self.make_func_add_line_table(self.ui.table_category_7))
        self.ui.Add_delta.clicked.connect(self.make_func_add_line_table(self.ui.table_delta_7))
        self.ui.calculate_7.clicked.connect(self.make_func_calculate_7(MODE_CALCULATE_7[0]))
        self.ui.calculate_with_delta.clicked.connect(self.make_func_calculate_7(MODE_CALCULATE_7[1]))
        self.ui.enter_categories_8.clicked.connect(self.enter_data_with_categories)
        self.ui.calculate_8.clicked.connect(self.calculate_8)
        self.ui.retry_8.clicked.connect(self.retry_8)
        self.var = FIRST_NAME_VAR
        self.ui.action_2.triggered.connect(self.add_pump)
        self.ui.action_4.triggered.connect(self.add_sup_pump)
        self.ui.action_7.triggered.connect(self.add_pipes)
        self.ui.action_delet.triggered.connect(self.delete_all_var)
        self.ui.action_save.triggered.connect(self.save_var_calculate)
        self.ui.action_new_var.triggered.connect(self.start_new_var)
        self.ui.action_xls.triggered.connect(self.save_to_xls)
        for list_objects in self.ui.dict_menu_var.values():
            for index, object_ui in enumerate(list_objects):
                if index == 1:
                    func = self.make_func_insert(list_objects[0].title())
                    object_ui.triggered.connect(func)
                elif index == 2:
                    func = self.make_func_delete_var(list_objects[0].title())
                    object_ui.triggered.connect(func)
        self.delete_func(FIRST_NAME_VAR)
        self.dict_action_table = {}
        self.add_copy_past_actions()

    def start_new_var(self):
        self.clean_all()
        self.delete_func(FIRST_NAME_VAR)
        self.var = FIRST_NAME_VAR
        self.ui.label.setText(f'Название варианта: {str(self.var)}')

    def add_copy_past_actions(self):
        list_table = [self.ui.tableWidget_charactiristics, self.ui.tableWidget_oil_properties, self.ui.table,
                      self.ui.tableWidget_2, self.ui.tableWidget, self.ui.table_date_7, self.ui.table_category_7,
                      self.ui.table_delta_7, self.ui.table_finish_7, self.ui.tableWidget_8]
        self.copy_action = CopySelectedCellsAction(list_table)
        self.past_action = PastSelectedCellsAction(list_table)
        self.addAction(self.copy_action)
        self.addAction(self.past_action)

    def save_to_xls(self):
        self.my_file_browser = MyFileBrowser(self.var)
        self.my_file_browser.show()

    def add_pipes(self):
        self.add_pipes_dialog = AddPipeDialogWindow()
        self.add_pipes_dialog.show()

    def add_pump(self):
        self.add_pump_dialog = AddPumpDialogWindow()
        self.add_pump_dialog.show()

    def add_sup_pump(self):
        self.add_sup_pump_dialog = AddSupPumpDialogWindow()
        self.add_sup_pump_dialog.show()

    def make_func_insert(self, var):

        def func_insert():
            self.insert_values(var)

        return func_insert

    def make_func_delete_var(self, var):

        def func_delete():
            self.delete_func(var)

        return func_delete

    def make_func_add_line_table(self, table):

        def add_func():
            index_table_widget = table.rowCount() + 1
            table.setRowCount(index_table_widget)
            item = QtWidgets.QTableWidgetItem(f'{index_table_widget}')
            font = QtGui.QFont()
            font.setFamily("Times New Roman")
            font.setPointSize(10)
            item.setFont(font)
            table.setVerticalHeaderItem(index_table_widget - 1, item)

        return add_func

    def insert_values_calculate_5(self, var_name):
        self.ui.label.setText(f'Название варианта: {str(var_name)}')
        dict_value = get_source_dict(var_name)
        for index, name_table in enumerate(LIST_WITH_NAME_VALUE_CHARACTIRISTIES):
            for name, value in dict_value.items():
                if name_table == name:
                    value_object = QtWidgets.QTableWidgetItem(str(value))
                    self.ui.tableWidget_charactiristics.setItem(index, 1, value_object)
        for index, name_table in enumerate(LIST_WITH_NAME_VALUE_OIL_PROPERTIES):
            for name, value in dict_value.items():
                if name_table == name:
                    value_object = QtWidgets.QTableWidgetItem(str(value))
                    self.ui.tableWidget_oil_properties.setItem(index, 1, value_object)
        source = CoordinatesTable.select().where(CoordinatesTable.var == var_name).get()
        json_coordinates = source.json_coordinates
        coordinates = json.loads(json_coordinates)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        item = QtWidgets.QTableWidgetItem(f'{1}')
        item.setFont(font)
        self.ui.table.setRowCount(1)
        self.ui.table_delta_7.setVerticalHeaderItem(0, item)
        for index, point in enumerate(coordinates):
            x = QtWidgets.QTableWidgetItem(str(point[0]))
            self.ui.table.setItem(index, 0, x)
            y = QtWidgets.QTableWidgetItem(str(point[1]))
            self.ui.table.setItem(index, 1, y)
            self.ui.table.setRowCount(index + 2)
            item = QtWidgets.QTableWidgetItem(f'{index + 2}')
            item.setFont(font)
            self.ui.table.setVerticalHeaderItem(index + 1, item)
        self.return_result_5(self.var)
        self.ui.frame_25.close()
        self.ui.pushButton_1.setVisible(True)
        self.ui.pushButton_2.setVisible(True)
        if get_state_var(self.var) != 0:
            self.add_button_show()

    def insert_values_calculate_7(self, var_name):
        self.ui.label_calc_var_7.setText(f'Название варианта: {str(var_name)}')
        self.ui.table_date_7.setColumnCount(2)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        item = QtWidgets.QTableWidgetItem('Имя')
        item.setFont(font)
        self.ui.table_date_7.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem('Значение')
        item.setFont(font)
        self.ui.table_date_7.setHorizontalHeaderItem(1, item)
        number_count = 1
        dict_value = get_source_dict(var_name)
        font.setPointSize(10)
        for name, value in dict_value.items():
            if name not in LIST_WITH_TABLE_VALUE_CALC_7[1]:
                continue
            self.ui.table_date_7.setRowCount(number_count)
            item = QtWidgets.QTableWidgetItem(f'{number_count}')
            item.setFont(font)
            self.ui.table_date_7.setVerticalHeaderItem(number_count - 1, item)
            index_name = LIST_WITH_TABLE_VALUE_CALC_7[1].index(name)
            name = QtWidgets.QTableWidgetItem(LIST_WITH_TABLE_VALUE_CALC_7[0][index_name])
            name.setFlags(QtCore.Qt.ItemIsEnabled)
            name.setFont(font)
            self.ui.table_date_7.setItem(number_count - 1, 0, name)
            value = QtWidgets.QTableWidgetItem(str(value))
            self.ui.table_date_7.setItem(number_count - 1, 1, value)
            number_count += 1
        self.ui.table_date_7.resizeColumnToContents(0)
        self.ui.table_date_7.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.ui.table_category_7.setRowCount(0)
        self.ui.table_category_7.clearContents()
        self.ui.table_delta_7.setRowCount(0)
        self.ui.table_delta_7.clearContents()
        self.ui.table_finish_7.setRowCount(0)
        self.ui.table_finish_7.clearContents()
        list_with_data_category = get_info_table_list(self.var, LIST_WITH_NAME_DATA_TABLE7[0])
        if list_with_data_category is None:
            return
        for index_list, list_info in enumerate(list_with_data_category):
            for index, value in enumerate(list_info):
                if index_list == 0:
                    self.ui.table_category_7.setRowCount(index + 1)
                    item = QtWidgets.QTableWidgetItem(f'{index + 1}')
                    item.setFont(font)
                    self.ui.table_category_7.setVerticalHeaderItem(index, item)
                value = QtWidgets.QTableWidgetItem(str(value))
                self.ui.table_category_7.setItem(index, index_list, value)
        for index, category in enumerate(list_with_data_category[0]):
            self.ui.table_delta_7.setRowCount(index + 1)
            item = QtWidgets.QTableWidgetItem(f'{index + 1}')
            item.setFont(font)
            self.ui.table_delta_7.setVerticalHeaderItem(index, item)
            category = QtWidgets.QTableWidgetItem(str(category))
            self.ui.table_delta_7.setItem(index, 0, category)
        list_with_data_delta = get_info_table_list(self.var, LIST_WITH_NAME_DATA_TABLE7[2])
        if list_with_data_delta is not None:
            for index, delta in enumerate(list_with_data_delta):
                delta = QtWidgets.QTableWidgetItem(str(delta))
                self.ui.table_delta_7.setItem(index, 1, delta)
        list_with_finish_data = get_info_table_list(self.var, LIST_WITH_NAME_DATA_TABLE7[1])
        if list_with_finish_data is None:
            return
        self.return_result_calc_7()

    def insert_values_8(self, var_name):
        self.ui.label_var_8.setText(f'Назавние варианта: {var_name}')
        dict_value = get_source_dict(var_name)
        if LIST_WITH_NAME_SOURCE_VALUE_8[0] not in dict_value.keys() and LIST_WITH_NAME_SOURCE_VALUE_8[
            1] not in dict_value.keys():
            return None
        self.ui.lineEdit_hmin_8.setText(f'{dict_value[LIST_WITH_NAME_SOURCE_VALUE_8[0]]}')
        self.ui.lineEdit_a_.setText(f'{dict_value[LIST_WITH_NAME_SOURCE_VALUE_8[1]]}')
        self.return_result_calc_8(var_name)

    def insert_values(self, var_name):
        self.var = var_name
        self.clean_all()
        self.consequence_state(var_name)

    def save_var_calculate(self):
        if self.ui.tableWidget_2.rowCount() == 0:
            self.error_save_window = ErrorSaveDialogWindow()
            self.error_save_window.exec()
            return
        self.save_dialog_window = SaveDialogWindow()
        self.save_dialog_window.exec()
        new_name_var = self.save_dialog_window.return_name_var()
        if new_name_var is None:
            return
        for infor_var in ActionVarTable.select():
            if infor_var.var == new_name_var:
                self.delete_func(infor_var.var)
                break
        update_var_table(self.var, new_name_var)
        self.var = new_name_var
        new_name_action = FIRST_NAME_ACTION_VAR
        list_numbers_action = [int(var.name_action[-1]) for var in ActionVarTable.select()]
        list_numbers_action.sort()
        if list_numbers_action:
            number = list_numbers_action[-1] + 1
            new_name_action = FIRST_NAME_ACTION_VAR[0:-1] + str(number)
        actions = ActionVarTable(
            var=new_name_var,
            name_action=new_name_action
        )
        actions.save()
        self.ui.dict_menu_var[new_name_action] = []
        self.ui.dict_menu_var[new_name_action].append(QtWidgets.QMenu(parent=self, title=new_name_var))
        self.ui.dict_menu_var[new_name_action].append(QtWidgets.QAction(parent=self, text='Открыть'))
        self.ui.dict_menu_var[new_name_action].append(QtWidgets.QAction(parent=self, text='Удалить'))
        self.ui.dict_menu_var[new_name_action][0].addAction(self.ui.dict_menu_var[new_name_action][1])
        self.ui.dict_menu_var[new_name_action][0].addAction(self.ui.dict_menu_var[new_name_action][2])
        self.ui.menu.addMenu(self.ui.dict_menu_var[new_name_action][0])

        self.insert_values(self.var)

    def show_error_enter(self):
        self.error_dialog_enter_5 = ErrorDialogEnterWindow()
        self.error_dialog_enter_5.exec()

    def show_error_enter_number(self):
        self.error_enter_Number = ErrorEnterNumberDialogWindow()
        self.error_enter_Number.exec()

    def check_value(self, value_object):
        if value_object is None:
            self.show_error_enter()
            return None
        value = value_object.text()
        if value == '':
            self.show_error_enter()
            return None
        if check_data(value) is None:
            self.show_error_enter_number()
            return None
        else:
            return value

    def get_data_in_db_5(self):
        self.delete_func(FIRST_NAME_VAR)
        dict_with_value = {}
        for i in range(self.ui.tableWidget_charactiristics.rowCount()):
            value_object = self.ui.tableWidget_charactiristics.item(i, 1)
            value = self.check_value(value_object)
            if value is None:
                return None
            if type(value) == str and ',' in value:
                value = value.replace(',', '.')
            value_float = float(value)
            dict_with_value[LIST_WITH_NAME_VALUE_CHARACTIRISTIES[i]] = value_float
        for i in range(self.ui.tableWidget_oil_properties.rowCount()):
            value_object = self.ui.tableWidget_oil_properties.item(i, 1)
            value = self.check_value(value_object)
            if value is None:
                return None
            if type(value) == str and ',' in value:
                value = value.replace(',', '.')
            value_float = float(value)
            dict_with_value[LIST_WITH_NAME_VALUE_OIL_PROPERTIES[i]] = value_float
        list_with_coordinates = []
        for i in range(self.ui.table.rowCount()):
            x_object = self.ui.table.item(i, 0)
            y_object = self.ui.table.item(i, 1)
            if x_object is None or y_object is None:
                break
            x = self.check_value(x_object)
            if x is None:
                return None
            y = self.check_value(y_object)
            if y is None:
                return None
            if type(x) == str and ',' in x:
                x = x.replace(',', '.')
            elif type(y) == str and ',' in y:
                y = y.replace(',', '.')
            x_float = float(x)
            y_float = float(y)
            list_with_coordinates.append([x_float, y_float])
        if len(list_with_coordinates) < 2:
            self.show_error_enter()
            return None
        delta_z = list_with_coordinates[-1][1] - list_with_coordinates[0][1]
        dict_with_value['delta_z'] = delta_z
        if self.check_var(dict_with_value, list_with_coordinates) or get_state_var(self.var) == 0:
            self.clean_all()
            if self.var != FIRST_NAME_VAR:
                self.dialog_choose_var = ChooseVarDialog()
                self.dialog_choose_var.exec()
                if not self.dialog_choose_var.get_decision():
                    self.var = FIRST_NAME_VAR
                    self.ui.label.setText(f'Название варианта: {str(self.var)}')
                    create_new_data_var_5(self.var, list_with_coordinates, dict_with_value)
                else:
                    update_list_coordinates_to_db(list_with_coordinates, self.var)
                    update_dict_to_db(dict_with_value, self.var)
                    load_update_var_state(self.var, 0)
                    delete_data_7_8(self.var, 2)
            else:
                create_new_data_var_5(self.var, list_with_coordinates, dict_with_value)
            self.ui.tabWidget.removeTab(2)
            self.ui.tabWidget.removeTab(1)
            self.ui.pushButton_1.setVisible(False)
            self.ui.pushButton_2.setVisible(False)
            return True
        else:
            return False

    def show_graphs(self):
        draw_graph_in_calculate(self.var)
        self.draw_graph(self.var)

    def add_button_show(self):
        self.ui.shower.setVisible(True)
        self.ui.checkBox.setVisible(True)
        self.ui.checkBox_2.setVisible(True)

    def calculate_5(self):
        result_get_data = self.get_data_in_db_5()
        if result_get_data is None:
            return
        if result_get_data is True:
            self.calculator_5 = Calculate5(self.var)
            self.calculator_5.calculate_first_part()
            self.pump_dialog = PumpDialogWindow(self.var, self)
            self.pump_dialog.exec()
            if self.pump_dialog.get_decision() is None:
                return
            self.calculator_5.calculate_second_part()
            self.dn_dialog_2 = DnDialogWindow_2(self, self.var)
            self.dn_dialog_2.exec()
            if self.dn_dialog_2.get_decision() is None:
                return
            self.dn_dialog = DnDialogWindow(self, self.var)
            self.dn_dialog.exec()
            if self.dn_dialog.get_decision() is None:
                return
            self.calc = External(self)
            self.calc.start()

    def return_result_5(self, var):
        dict_value = get_source_dict(var)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.ui.tableWidget_2.setColumnCount(2)
        item = QtWidgets.QTableWidgetItem('Значение')
        item.setFont(font)
        self.ui.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem('Результат')
        item.setFont(font)
        self.ui.tableWidget_2.setHorizontalHeaderItem(1, item)
        n_max = 0
        n_min = 0
        font.setPointSize(10)
        for index, name_value in enumerate(LIST_WITH_VALUE):
            for name, value in dict_value.items():
                self.ui.tableWidget_2.setRowCount(index + 1)
                item = QtWidgets.QTableWidgetItem(f'{index + 1}')
                item.setFont(font)
                self.ui.tableWidget_2.setVerticalHeaderItem(index, item)
                if name == name_value:
                    if name_value == 'n_max':
                        n_max = value
                        name_to_table = LIST_WITH_NAME[index]
                    elif name_value == 'n_min':
                        n_min = value
                        name_to_table = LIST_WITH_NAME[index]
                    elif name_value == 'Q2':
                        m_pump = dict_value['m_pump']
                        name_to_table = LIST_WITH_NAME[index].format(n_max=n_max, m_pump=int(m_pump))
                    elif name_value == 'Q1':
                        m_pump = dict_value['m_pump']
                        m_pump -= 1
                        name_to_table = LIST_WITH_NAME[index].format(n_max=n_max, m_pump=int(m_pump))
                    elif name_value == 'H_n_max_m_pump':
                        m_pump = dict_value['m_pump']
                        name_to_table = LIST_WITH_NAME[index].format(n_max=n_max, m_pump=int(m_pump))
                    elif name_value == 'tau1':
                        name_to_table = LIST_WITH_NAME[index].format(n_max=n_min)
                    elif name_value == 'tau2':
                        name_to_table = LIST_WITH_NAME[index].format(n_max=n_max)
                    else:
                        name_to_table = LIST_WITH_NAME[index]
                    name_table_to_ui = QtWidgets.QTableWidgetItem(name_to_table)
                    name_table_to_ui.setFlags(QtCore.Qt.ItemIsEnabled)
                    name_table_to_ui.setFont(font)
                    value_table_to_ui = QtWidgets.QTableWidgetItem(str(value))
                    self.ui.tableWidget_2.setItem(index, 0, name_table_to_ui)
                    self.ui.tableWidget_2.setItem(index, 1, value_table_to_ui)

    def draw_graph(self, var):
        dict_value = get_source_dict(var)
        list_for_drawing = dict_value['list_coordinates_for_drawing']
        if self.ui.checkBox_2.isChecked():
            drawing_plt(list_for_drawing)
        if self.ui.checkBox.isChecked():
            self.dialog_graph_window = GraphDialogWindow()
            self.dialog_graph_window.exec()
            drawing_autocad(list_for_drawing)

    def erase_data(self):
        for index, name in enumerate(LIST_WITH_NAME_VALUE_CHARACTIRISTIES):
            value = QtWidgets.QTableWidgetItem('')
            self.ui.tableWidget_charactiristics.setItem(index, 1, value)
        for index, name in enumerate(LIST_WITH_NAME_VALUE_OIL_PROPERTIES):
            value = QtWidgets.QTableWidgetItem('')
            self.ui.tableWidget_oil_properties.setItem(index, 1, value)
        self.ui.table.clearContents()
        self.ui.table.setRowCount(1)
        self.ui.tableWidget_2.setRowCount(0)
        self.ui.tableWidget_2.clearContents()
        if self.var == FIRST_NAME_VAR:
            self.delete_func(FIRST_NAME_VAR)
        self.var = FIRST_NAME_VAR
        self.ui.label.setText(f'Название варианта: {FIRST_NAME_VAR}')
        self.ui.shower.setVisible(False)
        self.ui.checkBox.setVisible(False)
        self.ui.checkBox_2.setVisible(False)
        self.clean_all()

    def check_var(self, dict_with_value, coordinates_from_ui):
        source = SourceDataTable.get_or_none(SourceDataTable.var == self.var)
        if source is not None:
            source_json_value = source.json_data
            source_dict_value = json.loads(source_json_value)
        else:
            return True
        for key, value in source_dict_value.items():
            if key in dict_with_value.keys():
                if value != dict_with_value[key]:
                    return True
        source = CoordinatesTable.get_or_none(CoordinatesTable.var == self.var)
        if source is not None:
            json_coordinates = source.json_coordinates
            coordinates = json.loads(json_coordinates)
        else:
            return True
        if coordinates == coordinates_from_ui:
            return False
        else:
            return True

    def delete_func(self, var):
        source_var = ActionVarTable.get_or_none(ActionVarTable.var == var)
        if source_var is not None:
            action_name = source_var.name_action
            self.ui.dict_menu_var[action_name][0].removeAction(self.ui.dict_menu_var[action_name][1])
            self.ui.dict_menu_var[action_name][0].removeAction(self.ui.dict_menu_var[action_name][2])
            self.ui.dict_menu_var[action_name][0].deleteLater()
            del self.ui.dict_menu_var[action_name]
        delete_func(var)

    def delete_all_var(self):
        source_var = ActionVarTable.get_or_none()
        if source_var is None:
            return
        list_all_var = [FIRST_NAME_VAR]
        for source_var in ActionVarTable.select():
            list_all_var.append(source_var.var)
        for var in list_all_var:
            self.delete_func(var)
        self.clean_all()
        self.var = FIRST_NAME_VAR
        self.ui.label.setText(f'Название варианта: {str(self.var)}')

    def make_func_calculate_7(self, var_calc):

        def func_calculate_7():
            self.calculate_7(var_calc)

        return func_calculate_7

    def get_data_to_db_without_delta(self):
        list_with_data_category = []
        list_with_number_section = []
        list_with_length_section = []
        list_with_category_section = []
        for i in range(self.ui.table_category_7.rowCount()):
            number_section_object = self.ui.table_category_7.item(i, 0)
            length_section_object = self.ui.table_category_7.item(i, 1)
            category_section_object = self.ui.table_category_7.item(i, 2)
            if i > 1:
                if number_section_object is None or length_section_object is None or category_section_object is None:
                    break
            length_section = self.check_value(length_section_object)
            category_section = self.check_value(category_section_object)
            if length_section is None or category_section is None:
                return None
            if number_section_object is None:
                self.show_error_enter()
                return None
            number_section = number_section_object.text()
            if type(number_section) == str and ',' in number_section:
                number_section = number_section.replace(',', '.')
            elif type(length_section) == str and ',' in length_section:
                length_section = length_section.replace(',', '.')
            elif type(category_section) == str and ',' in category_section:
                category_section = category_section.replace(',', '.')
            number_section_str = number_section
            length_section_float = float(length_section)
            category_section_float = float(category_section)
            list_with_number_section.append(number_section_str)
            list_with_length_section.append(length_section_float)
            list_with_category_section.append(category_section_float)
        if len(list_with_number_section) != len(list_with_length_section) or len(list_with_number_section) != len(
                list_with_category_section):
            self.show_error_enter()
            return None
        if not list_with_number_section:
            self.show_error_enter()
            return None
        if list_with_number_section != [] and list_with_length_section != [] and list_with_category_section != []:
            list_with_data_category.append(list_with_number_section)
            list_with_data_category.append(list_with_length_section)
            list_with_data_category.append(list_with_category_section)
        if list_with_data_category:
            check_update_data_var_7(self.var, LIST_WITH_NAME_DATA_TABLE7[0], list_with_data_category)
        return True

    def insert_table_category_to_delta(self):
        list_with_data_category = get_info_table_list(self.var, LIST_WITH_NAME_DATA_TABLE7[0])
        if list_with_data_category is None:
            self.dialog_delta = DialogDeltaWindow()
            self.dialog_delta.exec()
            return
        self.ui.table_delta_7.setRowCount(0)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        for index, category in enumerate(list_with_data_category[0]):
            self.ui.table_delta_7.setRowCount(index + 1)
            item = QtWidgets.QTableWidgetItem(f'{index + 1}')
            item.setFont(font)
            self.ui.table_delta_7.setVerticalHeaderItem(index, item)
            category = QtWidgets.QTableWidgetItem(str(category))
            self.ui.table_delta_7.setItem(index, 0, category)

    def enter_data_with_categories(self):
        self.get_data_to_db_without_delta()
        self.insert_table_category_to_delta()

    def get_data_to_db_with_delta(self, list_with_category_data):
        list_data_delta = []
        for i in range(self.ui.table_delta_7.rowCount()):
            delta_object = self.ui.table_delta_7.item(i, 1)
            if i > 1:
                if delta_object is None:
                    break
            delta_section = self.check_value(delta_object)
            if delta_section is None:
                return None
            if type(delta_section) == str and ',' in delta_section:
                delta_section = delta_section.replace(',', '.')
            delta_float = float(delta_section)
            list_data_delta.append(delta_float)
        if len(list_data_delta) != len(list_with_category_data[0]):
            self.show_error_enter()
            return None
        if list_data_delta:
            check_update_data_var_7(self.var, LIST_WITH_NAME_DATA_TABLE7[2], list_data_delta)
        return True

    def calculate_7(self, var_calc):
        if var_calc == MODE_CALCULATE_7[0]:
            if self.get_data_to_db_without_delta() is None:
                return
            calculator_7 = Calculate7(self.var, var_calc)
            calculator_7.calculate_without_deltas()
            self.insert_table_category_to_delta()
        elif var_calc == MODE_CALCULATE_7[1]:
            list_category_data = self.check_data_categories()
            if list_category_data is False:
                self.dialog_delta = DialogDeltaWindow()
                self.dialog_delta.exec()
                return
            if self.get_data_to_db_with_delta(list_category_data) is None:
                return
            calculator_7 = Calculate7(self.var, var_calc)
            calculator_7.calculate_with_deltas()
        load_update_var_state(self.var, 2)
        self.return_result_calc_7()
        self.ui.tabWidget.insertTab(2, self.ui.tab_3, 'Режимы работы нефтепровода')
        self.insert_values_8(self.var)
        if check_list_late_source_data_8(self.var, LIST_WITH_NAME_DATA_TABLE7[1],
                                         LIST_WITH_NAME_DATA_TABLE7[0]) is False:
            delete_data_7_8(self.var, 1)
            self.ui.tableWidget_8.setRowCount(0)
            load_update_var_state(self.var, 2)

    def check_data_categories(self):
        result = get_info_table_list(self.var, LIST_WITH_NAME_DATA_TABLE7[0])
        if result is None:
            return False
        else:
            return result

    def return_result_calc_7(self):
        finish_data_list = get_info_table_list(self.var, name_value=LIST_WITH_NAME_DATA_TABLE7[1])
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        for index, list_data in enumerate(finish_data_list):
            number, delta, R1, Hmax, Hps, conformity = list_data
            self.ui.table_finish_7.setRowCount(index + 1)
            item = QtWidgets.QTableWidgetItem(f'{index + 1}')
            item.setFont(font)
            self.ui.table_finish_7.setVerticalHeaderItem(index, item)
            number = QtWidgets.QTableWidgetItem(str(number))
            self.ui.table_finish_7.setItem(index, 0, number)
            delta = QtWidgets.QTableWidgetItem(str(delta))
            self.ui.table_finish_7.setItem(index, 1, delta)
            R1 = QtWidgets.QTableWidgetItem(str(R1))
            self.ui.table_finish_7.setItem(index, 2, R1)
            Hmax = QtWidgets.QTableWidgetItem(str(Hmax))
            self.ui.table_finish_7.setItem(index, 3, Hmax)
            Hps = QtWidgets.QTableWidgetItem(str(Hps))
            self.ui.table_finish_7.setItem(index, 4, Hps)
            conformity = QtWidgets.QTableWidgetItem(str(conformity))
            self.ui.table_finish_7.setItem(index, 5, conformity)

    def calculate_8(self):
        dict_value = get_source_dict(self.var)
        a_ = self.ui.lineEdit_a_.text()
        h_min = self.ui.lineEdit_hmin_8.text()
        if a_ == '' or h_min == '':
            self.show_error_enter()
            return
        if check_data(a_) is None or check_data(h_min) is None:
            self.show_error_enter_number()
            return
        a_ = float(a_)
        h_min = float(h_min)
        dict_value['a_'] = a_
        dict_value['h_min'] = h_min
        update_dict_to_db(dict_value, self.var)
        calculation_modes_nps = CalculationModesNps(self.var)
        calculation_modes_nps.run()
        load_update_var_state(self.var, 3)
        self.return_result_calc_8(self.var)

    def return_result_calc_8(self, var):
        table_8 = get_table_list_8(var)
        if table_8 is None:
            return
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(10)
        for index_column, list_column in enumerate(table_8):
            if index_column == 0:
                self.ui.tableWidget_8.setColumnCount(1)
                item_1 = QtWidgets.QTableWidgetItem(f'Режим')
                self.ui.tableWidget_8.setHorizontalHeaderItem(index_column, item_1)
            elif index_column == len(table_8) - 1:
                self.ui.tableWidget_8.setColumnCount(index_column + index_column)
                item_1 = QtWidgets.QTableWidgetItem(f'Соответствие')
                self.ui.tableWidget_8.setHorizontalHeaderItem(index_column + index_column - 1, item_1)
            else:
                self.ui.tableWidget_8.setColumnCount(index_column + index_column + 2)
                delta_h = f'Δh{index_column}, м'.translate(NUMBER_LOW_INDEX)
                H = f'H{index_column}, м'.translate(NUMBER_LOW_INDEX)
                item_1 = QtWidgets.QTableWidgetItem(delta_h)
                item_2 = QtWidgets.QTableWidgetItem(H)
                item_2.setFont(font)
                self.ui.tableWidget_8.setHorizontalHeaderItem(index_column + index_column - 1, item_1)
                self.ui.tableWidget_8.setHorizontalHeaderItem(index_column + index_column, item_2)
            item_1.setFont(font)
            for index_line, values in enumerate(list_column):
                if index_column == 0:
                    self.ui.tableWidget_8.setRowCount(index_line + 1)
                    item = QtWidgets.QTableWidgetItem(f'{index_line + 1}')
                    item.setFont(font)
                    self.ui.tableWidget_8.setVerticalHeaderItem(index_line, item)
                    value_1 = QtWidgets.QTableWidgetItem(str(values))
                    self.ui.tableWidget_8.setItem(index_line, index_column, value_1)
                    continue
                if index_column == len(table_8) - 1:
                    value_1 = QtWidgets.QTableWidgetItem(str(values))
                    self.ui.tableWidget_8.setItem(index_line, index_column + index_column - 1, value_1)
                else:
                    value_1 = QtWidgets.QTableWidgetItem(str(values[0]))
                    self.ui.tableWidget_8.setItem(index_line, index_column + index_column - 1, value_1)
                    values_2 = QtWidgets.QTableWidgetItem(str(values[1]))
                    self.ui.tableWidget_8.setItem(index_line, index_column + index_column, values_2)
        self.ui.tableWidget_8.resizeRowsToContents()

    def retry_8(self):
        self.ui.lineEdit_a_.clear()
        self.ui.lineEdit_hmin_8.clear()

    def consequence_state(self, var):
        state = get_state_var(var)
        if state == 1:
            self.insert_values_calculate_5(var)
            self.insert_values_calculate_7(var)
            self.ui.tabWidget.insertTab(1, self.ui.tab_2, 'Перерасчёт стенки трубы')
        elif state == 2:
            self.insert_values_calculate_5(var)
            self.insert_values_calculate_7(var)
            self.ui.tabWidget.insertTab(1, self.ui.tab_2, 'Перерасчёт стенки трубы')
            self.insert_values_8(var)
            self.ui.tabWidget.insertTab(2, self.ui.tab_3, 'Режимы работы нефтепровода')
        else:
            self.insert_values_calculate_5(var)
            self.insert_values_calculate_7(var)
            self.ui.tabWidget.insertTab(1, self.ui.tab_2, 'Перерасчёт стенки трубы')
            self.insert_values_8(var)
            self.ui.tabWidget.insertTab(2, self.ui.tab_3, 'Режимы работы нефтепровода')

    def clean_all(self):
        self.ui.tabWidget.removeTab(2)
        self.ui.tabWidget.removeTab(1)
        self.ui.shower.setVisible(False)
        self.ui.checkBox.setVisible(False)
        self.ui.checkBox_2.setVisible(False)
        list_table = [self.ui.tableWidget_2, self.ui.table_category_7, self.ui.table_delta_7, self.ui.table_finish_7,
                      self.ui.tableWidget_8]
        for index, table in enumerate(list_table):
            if index == 0 or index == len(list_table) - 1:
                table.setRowCount(0)
                table.setColumnCount(0)
            else:
                table.setRowCount(1)
            table.clearContents()
        self.ui.lineEdit_a_.clear()
        self.ui.lineEdit_hmin_8.clear()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    file = QFile(":/dark.qss")
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    app.setStyleSheet(stream.readAll())
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
