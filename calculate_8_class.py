# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 19:13:20 2020

@author: stinc
"""
import numpy as np
import math as mt
from pprint import pprint
from calculate_mode import calculate_mode_transportation
from settings import get_source_dict, update_dict_to_db, get_info_table_list, check_update_table_list_8_to_db, \
    load_list_data_to_check_table
from calculate_7_class import LIST_WITH_NAME_DATA_TABLE7


def find_number_nps_number_pump(var):
    dict_value = get_source_dict(var)
    number_nps = dict_value['n_nps_first_section']
    number_pump = int(dict_value['m_pump'])
    return number_nps, str(number_pump), dict_value


class CalculationModesNps:
    def __init__(self, var):
        self.var = var
        self.Na = 1

    def calc_all_data_coordinates(self, list_with_coordinates_nps, number_nps):
        self.section_length = list_with_coordinates_nps[number_nps][0] - list_with_coordinates_nps[0][0]
        self.height_difference = list_with_coordinates_nps[number_nps][1] - list_with_coordinates_nps[0][1]
        self.list_with_lenth_between_nps = []
        self.list_with_height_between_nps = []
        for index, coordinates_nps in enumerate(list_with_coordinates_nps):
            if index + 1 > number_nps:
                break
            lenth_between_npc = list_with_coordinates_nps[index + 1][0] - list_with_coordinates_nps[index][0]
            height_between_npc = list_with_coordinates_nps[index + 1][1] - list_with_coordinates_nps[index][1]
            self.list_with_lenth_between_nps.append(lenth_between_npc)
            self.list_with_height_between_nps.append(height_between_npc)

    def create_list_lenth_height_for_1_ps(self, dict_value):
        self.list_with_lenth_between_nps = []
        self.list_with_height_between_nps = []
        self.section_length = float(dict_value['L'])
        self.height_difference = float(dict_value['delta_z'])
        self.list_with_lenth_between_nps.append(float(dict_value['L']))
        self.list_with_height_between_nps.append(float(dict_value['delta_z']))

    def find_hmax_nps(self, list_coordinates_nps):
        list_with_lenth_sections = get_info_table_list(self.var, LIST_WITH_NAME_DATA_TABLE7[0])[1]
        list_with_data_7 = get_info_table_list(self.var, LIST_WITH_NAME_DATA_TABLE7[1])
        list_with_hmax_sections = [list_data_section[3] for list_data_section in list_with_data_7]
        list_check_list = [list_with_lenth_sections, list_with_hmax_sections]
        load_list_data_to_check_table(list_check_list, self.var)
        self.list_with_hmax_nps = []
        x1 = 0
        x2 = 0
        for index, lenth_section in enumerate(list_with_lenth_sections):
            x2 += lenth_section
            for coordinates_nps in list_coordinates_nps:
                if x1 <= coordinates_nps[0] <= x2:
                    self.list_with_hmax_nps.append(list_with_hmax_sections[index])
            x1 = x2
        self.list_with_hmax_sections = [float(hmax) for hmax in self.list_with_hmax_nps]

    def preparation_initial_data(self):
        number_nps, number_pump, dict_value = find_number_nps_number_pump(self.var)
        self.modes = calculate_mode_transportation(number_nps, number_pump)
        list_coordinates_nps = dict_value['list_coordinates_nps']
        if number_nps > 1:
            self.calc_all_data_coordinates(dict_value['list_coordinates_nps'], number_nps)
        else:
            self.create_list_lenth_height_for_1_ps(dict_value)
        self.find_hmax_nps(list_coordinates_nps)
        self.Dvn = dict_value['Dvn'] * 10 ** (-3)
        self.density = dict_value['density_t']
        self.vis = dict_value['vis_t'] * 10 ** (-6)
        self.Qm = dict_value['Q_nom_m']
        self.Qn = dict_value['Q_nom_s']
        self.ka = dict_value['k_a']
        self.am = dict_value['a_m']
        self.bm = dict_value['b_m']
        self.ap = dict_value['a_s']
        self.bp = dict_value['b_s']
        self.a_ = dict_value['a_']
        self.h_min = dict_value['h_min']
        self.host = dict_value['h_ost']
        self.m_n = int(number_pump)
        self.number_nps = number_nps

    def preliminary_calculations(self):
        # part 1
        self.n = self.m_n * self.number_nps
        self.Q1nm = self.Qm * 0.8
        self.Q2nm = self.Qm * 1.2
        self.Q1n = self.Qn * 0.8
        self.Q2n = self.Qn * 1.2
        self.w = 4 * self.Qm / (3600 * mt.pi * self.Dvn)
        self.Re = self.w * self.Dvn / self.vis
        self.k = self.ka / (self.Dvn * 10 ** 3)
        self.lakv = 0.11 * (self.ka / (self.Dvn * 10 ** 3)) ** 0.25
        self.Re1 = 10 / self.k
        self.Re2 = 500 / self.k
        if self.Re < self.Re1:
            self.m1 = 1
            self.beta_1 = 0.0802 * 10 ** (0.127 * mt.log10(self.k) - 0.627)
        elif self.Re < self.Re2:
            self.m1 = 0.25
            self.beta_1 = 0.0246
        else:
            self.m1 = 0.123
            self.beta_1 = 4.15
        if self.Re > self.Re2:
            self.m2 = 0
            self.beta_2 = 0.0826 * self.lakv
        elif self.Re > self.Re1:
            self.m2 = 0.123
            self.beta_2 = 0.0802 * 10 ** (0.127 * mt.log10(self.k) - 0.627)
        else:
            self.m2 = 0.25
            self.beta_2 = 0.0246
        # part 2
        self.f = 1.02 * self.beta_2 * ((self.vis ** self.m2) / (self.Dvn ** (5 - self.m2)))
        self.Bp_ = ((self.Q2n - self.Q1n) * (- self.a_ + self.bp * (self.Q2n + self.Q1n))) / \
                   ((self.Q2n ** (2 - self.m2)) - (self.Q1n ** (2 - self.m2)))
        self.Bp = 3600 ** (2 - self.m2) * self.Bp_
        self.Ap = self.ap + self.a_ * self.Q2n - self.bp * self.Q2n ** 2 + self.Bp_ * self.Q2n ** (2 - self.m2)
        self.Bm_ = ((self.Q2nm - self.Q1nm) * (- self.a_ + self.bm * (self.Q2nm + self.Q1nm))) / \
                   ((self.Q2nm ** (2 - self.m2)) - (self.Q1nm ** (2 - self.m2)))
        self.Bm = (3600 ** (2 - self.m2)) * self.Bm_
        self.Am = self.am + self.a_ * self.Q2nm - self.bm * self.Q2nm ** 2 + self.Bm_ * self.Q2nm ** (2 - self.m2)
        self.Q = ((self.Na * self.Ap + self.n * self.Am - self.height_difference - self.Na * self.host) /
                  (self.Na * self.Bp + self.f * self.section_length * 1000 + self.n * self.Bm)) ** (1 / (2 - self.m2))
        # part 3
        if self.Re > self.Re2:
            self.m1 = 0.123
            self.m2 = 0
            self.beta_1 = 0.0802 * 10 ** (0.127 * mt.log10(self.k) - 0.627)
            self.beta_2 = 0.0826 * self.lakv
        elif self.Re > self.Re1:
            self.m1 = 0.25
            self.m2 = 0.123
            self.beta_1 = 0.0246
            self.beta_2 = 0.0802 * 10 ** (0.127 * mt.log10(self.k) - 0.627)
        else:
            self.m1 = 1
            self.m2 = 0.25
            self.beta_1 = 4.15
            self.beta_2 = 0.0246
        if self.m2 == 0:
            self.Re_comparisons = 500 / self.k
        elif self.m2 == 0.123:
            self.Re_comparisons = 10 / self.k
        else:
            self.Re_comparisons = 2320

    def mode_check(self):
        self.list_with_Re_first = []
        numbers_n = list(range(self.n))
        for number in numbers_n:
            number += 1
            Q = ((self.Na * self.Ap + number * self.Am - self.height_difference - self.Na * self.host) /
                 (self.Na * self.Bp + self.f * self.section_length * 1000 + number * self.Bm))
            if Q < 0:
                Q = 0
            Q = Q ** (1 / (2 - self.m2))
            w = Q * 4 / (mt.pi * self.Dvn)
            re = w * self.Dvn / self.vis
            self.list_with_Re_first.append(re)

    def calculation_totals(self):
        self.list_with_Bp = []
        self.list_with_Ap = []
        self.list_with_Bm = []
        self.list_with_Am = []
        self.list_with_Q = []
        self.list_with_Re = []
        self.list_with_f = []
        for index, Re in enumerate(self.list_with_Re_first):
            n = index + 1
            if Re > self.Re_comparisons:
                m = self.m2
                beta = self.beta_2
            else:
                m = self.m1
                beta = self.beta_1
            f = 1.02 * beta * ((self.vis ** m) / (self.Dvn ** (5 - m)))
            self.list_with_f.append(f)
            Bp_ = ((self.Q2n - self.Q1n) * (- self.a_ + self.bp * (self.Q2n + self.Q1n))) / \
                  ((self.Q2n ** (2 - m)) - (self.Q1n ** (2 - m)))
            Bp = 3600 ** (2 - m) * Bp_
            self.list_with_Bp.append(Bp)
            Ap = self.ap + self.a_ * self.Q2n - self.bp * self.Q2n ** 2 + Bp_ * self.Q2n ** (2 - m)
            self.list_with_Ap.append(Ap)
            Bm_ = ((self.Q2nm - self.Q1nm) * (- self.a_ + self.bm * (self.Q2nm + self.Q1nm))) / \
                  (self.Q2nm ** (2 - m) - self.Q1nm ** (2 - m))
            Bm = (3600 ** (2 - m)) * Bm_
            self.list_with_Bm.append(Bm)
            Am = self.am + self.a_ * self.Q2nm - self.bm * self.Q2nm ** 2 + Bm_ * self.Q2nm ** (2 - m)
            self.list_with_Am.append(Am)
            Q = ((self.Na * Ap + n * Am - self.height_difference - self.Na * self.host) /
                 (self.Na * Bp + f * self.section_length * 1000 + n * Bm)) ** (
                        1 / (2 - m))
            self.list_with_Q.append(Q)
            w = 4 * Q / (mt.pi * self.Dvn)
            Re = w * self.Dvn / self.vis
            self.list_with_Re.append(Re)

    def calculation_modes(self):
        self.table = []
        for index, mode in enumerate(self.modes):
            if index == 0:
                self.table.append([])
            mode = [int(num) for num in mode]
            string_mode = ''
            for index_m, num in enumerate(mode):
                if index_m == len(mode) - 1:
                    string_mode += f'{num}'
                    break
                string_mode += f'{num} - '
            self.table[0].append(string_mode)
            number_pump = sum(mode)
            index_list = number_pump - 1
            Re = self.list_with_Re[index_list]
            Q = self.list_with_Q[index_list]
            Ap = self.list_with_Ap[index_list]
            Bp = self.list_with_Bp[index_list]
            Am = self.list_with_Am[index_list]
            Bm = self.list_with_Bm[index_list]
            f = self.list_with_f[index_list]
            conformity = 'да'
            if Re > self.Re_comparisons:
                m = self.m2
            else:
                m = self.m1
            for index_a, amount_pump in enumerate(mode):
                if index == 0:
                    self.table.append([])
                if index_a == 0:
                    delta_H = Ap - Bp * (Q / 2) ** (2 - m)
                else:
                    delta_H = H - self.list_with_height_between_nps[index_a - 1] - f * Q ** (2 - m) * \
                              self.list_with_lenth_between_nps[index_a - 1] * 1000
                H = delta_H + amount_pump * (Am - Bm * Q ** (2 - m))
                self.table[index_a + 1].append([delta_H, H])
                if H <= self.list_with_hmax_nps[index_a] and delta_H >= self.h_min and conformity == 'да':
                    continue
                else:
                    conformity = 'нет'
            if index == 0:
                self.table.append([])
            self.table[len(mode) + 1].append(conformity)
        check_update_table_list_8_to_db(self.table, self.var)

    def run(self):
        self.preparation_initial_data()
        self.preliminary_calculations()
        self.mode_check()
        self.calculation_totals()
        self.calculation_modes()
