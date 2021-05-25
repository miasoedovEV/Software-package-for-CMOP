# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 19:13:20 2020

@author: stinc
"""
from decimal import Decimal
from logic_modules.settings import get_source_dict, check_update_data_var_7, get_info_table_list

LIST_WITH_NAME_DATA_TABLE7 = ['list_with_data_category', 'finish_data_list', 'list_with_data_delta']
MODE_CALCULATE_7 = ['without_delta', 'with_delta']
G = Decimal('9.81')


class Calculate7:
    def __init__(self, var, var_calc):
        self.var = var
        self.dict_values = get_source_dict(self.var)
        for name_value, value in self.dict_values.items():
            if name_value == 'Dvn':
                self.Dvn = Decimal(f'{value}')
            elif name_value == 'delta':
                self.delta = Decimal(f'{value}')
            elif name_value == 'R1n':
                self.R1n = Decimal(f'{value}')
            elif name_value == 'k1':
                self.k1 = Decimal(f'{value}')
            elif name_value == 'np':
                self.np = Decimal(f'{value}')
            elif name_value == 'kn':
                self.kn = Decimal(f'{value}')
            elif name_value == 'm_kaf':
                self.m_kaf = Decimal(f'{value}')
            elif name_value == 'density_t':
                self.density_t = Decimal(f'{value}')
            elif name_value == 'H_for_calc_delta':
                self.Hps = Decimal(f'{value}')
        self.list_with_data_categories = get_info_table_list(self.var, LIST_WITH_NAME_DATA_TABLE7[0])
        self.site_categories_d = [Decimal(f'{my}') for my in self.list_with_data_categories[2]]
        if var_calc == MODE_CALCULATE_7[1]:
            self.list_data_deltas = get_info_table_list(self.var, LIST_WITH_NAME_DATA_TABLE7[2])

    def calculate_R1(self):
        self.list_R1 = []
        for category in self.site_categories_d:
            dec = category * self.R1n / (self.k1 * self.kn)
            self.list_R1.append(dec)

    def calculate_without_deltas(self):
        self.calculate_R1()

        Hmax = []

        for R1 in self.list_R1:
            dec = 2 * self.delta * R1 * 10 ** 6 / (self.density_t * G * self.np * self.Dvn)
            Hmax.append(dec)

        list_parcels_calculation = []
        conformity = 'да'
        for index, hmax in enumerate(Hmax):
            if self.Hps > hmax:
                conformity = 'нет'
            list_parcels_calculation.append(
                [str(self.list_with_data_categories[2][index]), float(self.delta), float(self.list_R1[index]),
                 float(hmax), float(self.Hps), conformity])
            conformity = 'да'
        check_update_data_var_7(self.var, LIST_WITH_NAME_DATA_TABLE7[1], list_parcels_calculation)

    def calculate_with_deltas(self):
        list_parcels_recalculation_D = [Decimal(str(delta)) for delta in self.list_data_deltas]
        self.calculate_R1()

        Hmax = []
        for index, R1 in enumerate(self.list_R1):
            dec = 2 * list_parcels_recalculation_D[index] * R1 * 10 ** 6 / (self.density_t * G * self.np * self.Dvn)
            Hmax.append(dec)

        list_parcels_recalculation = []
        conformity = 'да'
        for index, hmax in enumerate(Hmax):
            if self.Hps > hmax:
                conformity = 'нет'
            list_parcels_recalculation.append(
                [str(self.list_with_data_categories[2][index]), self.list_data_deltas[index],
                 float(self.list_R1[index]),
                 float(hmax), float(self.Hps), conformity])
            conformity = 'да'
        check_update_data_var_7(self.var, LIST_WITH_NAME_DATA_TABLE7[1], list_parcels_recalculation)
