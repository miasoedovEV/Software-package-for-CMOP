# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'design_probe.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

import xlwt
from logic_modules.settings import get_source_dict, get_info_table_list, get_table_list_8, LIST_NAME_DATA_TABLE7, \
    LIST_WITH_NAME, LIST_WITH_VALUE

LIST_WITH_TITLE_COLUMNS_7 = ['Категоря участка', 'Толщина стенки, мм', 'R1, МПа', 'Hmax, м', 'Hпс, м', 'Соответствие']

from os import path


class CreatorXlsFile:
    def __init__(self, file_path, file_name, var):
        self.file_path = file_path
        self.file_name = file_name
        self.var = var
        self.dict_values = get_source_dict(self.var)
        self.finish_list_7 = get_info_table_list(self.var, LIST_NAME_DATA_TABLE7[0])
        self.table_list_8 = get_table_list_8(self.var)

    def create_xls_file(self):
        self.book = xlwt.Workbook('utf8')
        self.font = xlwt.easyxf('font: height 160,name Arial,colour_index black, bold off,\
            italic off; align: wrap on, vert top, horiz left;\
            pattern: pattern solid, fore_colour white;')
        self.sheet_1 = self.book.add_sheet('Расстановка НПС')
        self.sheet_2 = self.book.add_sheet('Перерасчёт стенки трубопровода')
        self.sheet_3 = self.book.add_sheet('Расчёт режимов')
        self.sheet_1.col(0).width = 8000

    def enter_data_1(self):
        n_max = 0
        n_min = 0
        self.sheet_1.write(0, 0, 'Значение', self.font)
        self.sheet_1.write(0, 1, 'Результат', self.font)
        for index, name_value in enumerate(LIST_WITH_VALUE):
            index_line = index + 1
            for name, value in self.dict_values.items():
                if name == name_value:
                    if name_value == 'n_max':
                        n_max = value
                    elif name_value == 'n_min':
                        n_min = value
                    elif name_value == 'Q2':
                        m_pump = self.dict_values['m_pump']
                        LIST_WITH_NAME[index] = LIST_WITH_NAME[index].format(n_max=n_max, m_pump=int(m_pump))
                    elif name_value == 'Q1':
                        m_pump = self.dict_values['m_pump']
                        m_pump -= 1
                        LIST_WITH_NAME[index] = LIST_WITH_NAME[index].format(n_max=n_max, m_pump=int(m_pump))
                    elif name_value == 'H_n_max_m_pump':
                        m_pump = self.dict_values['m_pump']
                        LIST_WITH_NAME[index] = LIST_WITH_NAME[index].format(n_max=n_max, m_pump=int(m_pump))
                    elif name_value == 'tau1':
                        LIST_WITH_NAME[index] = LIST_WITH_NAME[index].format(n_max=n_min)
                    elif name_value == 'tau2':
                        LIST_WITH_NAME[index] = LIST_WITH_NAME[index].format(n_max=n_max)
                    self.sheet_1.write(index_line, 0, LIST_WITH_NAME[index], self.font)
                    self.sheet_1.write(index_line, 1, value, self.font)
        self.sheet_1.write(0, 2, 'Координаты ПС', self.font)
        self.sheet_1.write(0, 3, 'x', self.font)
        self.sheet_1.write(0, 4, 'y', self.font)
        if 'list_coordinates_nps' not in self.dict_values.keys():
            return
        for index, coordinates in enumerate(self.dict_values['list_coordinates_nps']):
            self.sheet_1.write(index + 1, 3, coordinates[0], self.font)
            self.sheet_1.write(index + 1, 4, coordinates[1], self.font)

    def enter_2(self):
        for index in range(len(self.finish_list_7)):
            self.sheet_2.row(index).height = 500
        for index, name in enumerate(LIST_WITH_TITLE_COLUMNS_7):
            self.sheet_2.write(0, index, name, self.font)
        for index, list_data in enumerate(self.finish_list_7):
            index += 1
            for index_2, value in enumerate(list_data):
                self.sheet_2.write(index, index_2, value, self.font)

    def enter_3(self):
        for index_column, list_column in enumerate(self.table_list_8):
            if index_column == 0:
                self.sheet_3.write(0, index_column, 'Режим', self.font)
            elif index_column == len(self.table_list_8) - 1:
                self.sheet_3.write(0, index_column + index_column - 1, 'Соответствие', self.font)
            else:
                self.sheet_3.write(0, index_column + index_column - 1, f'Δh{index_column}, м', self.font)
                self.sheet_3.write(0, index_column + index_column, f'H{index_column}, м', self.font)
            for index_line, values in enumerate(list_column):
                index_line += 1
                if index_column == 0:
                    self.sheet_3.write(index_line, index_column, values, self.font)
                    continue
                if index_column == len(self.table_list_8) - 1:
                    self.sheet_3.write(index_line, index_column + index_column - 1, values, self.font)
                else:
                    value_1 = str(values[0])
                    self.sheet_3.write(index_line, index_column + index_column - 1, value_1, self.font)
                    values_2 = str(values[1])
                    self.sheet_3.write(index_line, index_column + index_column, values_2, self.font)

    def save(self):
        self.create_xls_file()
        if self.dict_values is not None:
            self.enter_data_1()
        if self.finish_list_7 is not None:
            self.enter_2()
        if self.table_list_8 is not None:
            self.enter_3()
        save_path = path.join(self.file_path, self.file_name)
        self.book.save(save_path)
