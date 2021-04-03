# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 19:13:20 2020

@author: stinc
"""
import time

import matplotlib.pyplot as plt
from decimal import getcontext, Decimal, ROUND_HALF_UP
import numpy as np
import math
from models import MainPumpsTable, SupportPumpsTable, GraphW0, DnTable
from settings import get_source_dict, update_dict_to_db, get_list_coordinates
import json
from multiprocessing.pool import ThreadPool

pool = ThreadPool(processes=1)

COLORS = ['black', 'red', 'green', 'grey', 'blue']


def plot_show(x, y, label_x, label_y, plot_title):
    plt.figure()
    plt.plot(x, y)
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.title(plot_title)
    plt.show()


def many_plot(x, ys, label_x, label_y, labels, title, colors):
    plt.figure()
    for i, y in enumerate(ys):
        plt.plot(x, y, colors[i], label=labels[i])
    plt.xlabel(label_x)
    plt.ylabel(label_y)
    plt.title(title)
    plt.legend()
    plt.show()


class Calculate5:
    def __init__(self, var):
        self.var = var
        self.dict_value = get_source_dict(self.var)
        for name, value in self.dict_value.items():
            if name == 'L':
                self.L = value
            elif name == 'section_length':
                self.section_length = value
            elif name == 'operating_pressure':
                self.operating_pressure = value
            elif name == 'Gg':
                self.Gg = value
            elif name == 'knp':
                self.knp = value
            elif name == 'Tr':
                self.Tr = value
            elif name == 'h_ost':
                self.h_ost = value
            elif name == 'm_pump':
                self.m_pump = value
            elif name == 'Np':
                self.Np = value
            elif name == 'density':
                self.density = value
            elif name == 'vis_1':
                self.vis_1 = value
            elif name == 'vis_2':
                self.vis_2 = value
            elif name == 'T1':
                self.T1 = value
            elif name == 'T2':
                self.T2 = value
            elif name == 'delta_z':
                self.delta_z = value
        self.G = 9.81

    def calculate_first_part(self):
        # Блок расчёта

        # 2.Нахождение  вязкости и температуры перекачки
        getcontext().prec = 50
        ksi = 1.825 - 0.001315 * self.density  # температурная поправка
        self.density_t = self.density + ksi * (293 - self.Tr)  # расч плотность
        B = np.log10(np.log10(self.vis_2 + 0.8) / np.log10(self.vis_1 + 0.8)) / (
                np.log10(self.T2) - np.log10(self.T1))

        At = ((self.Tr / self.T1) ** B) * np.log10(self.vis_1 + 0.8)
        self.vis_t = (10 ** At) - 0.8
        # Построение графика

        self.T_k = list(range(273, 310, 5))  # данные для построения диаграммы изменений плотности от температуры

        self.vis_T = [(10 ** ((t_k / self.T1) ** B * np.log10(self.vis_1 + 0.8))) - 0.8 for t_k in
                      self.T_k]  # данные для вискограммы
        # Оперделение годовой пропускной способности

        # Определение часовой и секундной производительности
        Gg = self.Gg * self.knp  # годовая пропускная способность
        self.Q_hour = Gg * 10 ** 9 / (8400 * self.density_t)  # часовая производителбность м№3/c
        list_with_value = [['density_t', self.density_t], ['vis_t', self.vis_t], ['Q_hour', self.Q_hour],
                           ['T_k', self.T_k], ['vis_T', self.vis_T]]
        for name, value in list_with_value:
            self.dict_value[name] = value
        update_dict_to_db(self.dict_value, self.var)

    def check_pump(self):
        a = None
        b = None
        self.dict_value = get_source_dict(self.var)
        for name, value in self.dict_value.items():
            if name == 'a_m':
                a = value
            elif name == 'b_m':
                b = value
        return a, b

    def calculate_second_part(self):
        self.a_m, self.b_m = self.check_pump()
        if self.a_m is None or self.b_m is None:
            indicate = False
            for info in MainPumpsTable.select():
                if info.Q_nom * 1.2 < self.Q_hour:
                    continue
                if info.kaf != 1:
                    continue
                else:
                    self.hm = info.a - info.b * self.Q_hour ** 2
                    for info_s in SupportPumpsTable.select():
                        if info_s.Q_nom * 1.2 < (self.Q_hour / 2):
                            continue
                        self.hp = info_s.a - info_s.b * (self.Q_hour / 2) ** 2
                        self.P = self.density_t * self.G * (self.hp + self.m_pump * self.hm) * 10 ** (-6)
                        brand = info.brand
                        impeller_diameter = info.impeller_diameter
                        self.a_m = info.a
                        self.b_m = info.b
                        pump_suport_brand = info_s.brand
                        pump_suport_impeller_diameter = info_s.impeller_diameter
                        self.ap = info_s.a
                        self.bp = info_s.b
                        Q_nom_m = info.Q_nom
                        Q_nom_p = info_s.Q_nom
                        if self.P <= self.operating_pressure:
                            indicate = True
                            break
                if indicate:
                    list_with_value = [['brand_pump_m', brand], ['d_work_m', impeller_diameter], ['Q_nom_m', Q_nom_m],
                                       ['a_m', self.a_m], ['b_m', self.b_m]]
                    for name, value in list_with_value:
                        self.dict_value[name] = value
                    break
        else:
            self.hm = self.a_m - self.b_m * self.Q_hour ** 2
            for info_s in SupportPumpsTable.select():
                if info_s.Q_nom * 1.2 < (self.Q_hour / 2):
                    continue
                self.hp = info_s.a - info_s.b * (self.Q_hour / 2) ** 2
                self.P = self.density_t * self.G * (self.hp + self.m_pump * self.hm) * 10 ** (-6)
                pump_suport_brand = info_s.brand
                pump_suport_impeller_diameter = info_s.impeller_diameter
                self.ap = info_s.a
                self.bp = info_s.b
                Q_nom_p = info_s.Q_nom
                if self.P <= self.operating_pressure:
                    break
        list_with_value = [['brand_pump_s', pump_suport_brand], ['d_work_s', pump_suport_impeller_diameter],
                           ['Q_nom_s', Q_nom_p], ['a_s', self.ap], ['b_s', self.bp]]
        self.Hst = self.m_pump * self.hm
        for name, value in list_with_value:
            self.dict_value[name] = value
        # Определение диаметра и толщины стенки трубопровода
        info_graph = GraphW0.select().get()
        Q_graph = json.loads(info_graph.json_Q)
        w0_graph = json.loads(info_graph.json_w0)

        # составление уравнения для нахлждения скорости
        B = np.polyfit(Q_graph, w0_graph, 2)
        W = B[0] * self.Q_hour ** 2 + B[1] * self.Q_hour + B[2]

        # Вычисление диаметра
        D0 = (4 * self.Q_hour / (3600 * np.pi * W)) ** 0.5
        info_dn = DnTable.select().get()
        Dn_list = json.loads(info_dn.json_dn)
        for dn in Dn_list:
            if dn < D0 * 10 ** 3:
                continue
            else:
                self.Dn = dn
                break
        else:
            self.Dn = 1220
        self.dict_value['Dn'] = self.Dn
        update_dict_to_db(self.dict_value, self.var)

    def calculate_third_part(self):
        self.dict_value = get_source_dict(self.var)
        for name, value in self.dict_value.items():
            if name == 'R1n':
                R1n = value
            elif name == 'k1':
                k1 = value
            elif name == 'np':
                np = value
            elif name == 'kn':
                kn = value
            elif name == 'm_kaf':
                m_kaf = value
            elif name == 'k_a':
                k_a = value
            elif name == 'Dn':
                self.Dn = value
        R1 = R1n * m_kaf / (k1 * kn)

        delta = np * self.P * self.Dn / (2 * (R1 + np * self.P))

        delta_n = math.ceil(delta)

        self.Dvn = self.Dn - 2 * delta_n

        # Гидравлический расчёт
        w = 4 * self.Q_hour / (3600 * math.pi * (self.Dvn * 10 ** (-3)) ** 2)

        self.k_ = k_a / self.Dvn

        self.Re1 = 10 / self.k_

        self.Re2 = 500 / self.k_

        self.Re = w * self.Dvn * 10 ** (-3) / (self.vis_t * 10 ** (-6))
        if self.Re < 2300:
            m = 1
            lambda_ = 64 / self.Re
        elif 2300 < self.Re < self.Re1:
            m = 0.25
            lambda_ = 0.3164 / (self.Re ** 0.25)
        elif self.Re1 < self.Re < self.Re2:
            m = 0.123
            lambda_ = 0.11 * (68 / self.Re + self.k_) ** 0.25
        else:
            m = 0
            lambda_ = 0.11 * self.k_ ** 0.25
        # Потери напора на трение
        self.h_t = lambda_ * (self.L * 10 ** 3 * w ** 2) / (self.Dvn * 10 ** (-3) * 2 * self.G)

        # Суммарные потери напора
        self.N_a = round(self.L / self.section_length)

        self.H = 1.02 * self.h_t + self.delta_z + self.N_a * self.h_ost

        # Гидравлический уклон
        self.i = self.h_t / (self.L * 10 ** 3)

        # Определение числа перекачивающих станций
        n0 = (self.H - self.N_a * self.hp) / self.Hst

        n_min = math.floor(n0)

        self.n_max = math.ceil(n0)

        if self.n_max == 1:
            self.N_a = 1

        # Расчёт длины лупинга
        kaf_w = 1 / 2 ** (2 - m)

        l_l = ((n0 - n_min) * self.Hst) / (1.02 * self.i * (1 - kaf_w))

        self.N5_M3 = []
        self.N6_M3 = []
        self.N6_M2 = []
        self.Hs = []
        self.Hs_with_looping = []
        self.q_list = list(range(int(self.Q_hour - 1000), int(self.Q_hour + 4000), 500))
        for index, q in enumerate(self.q_list):
            hm = self.a_m - self.b_m * q ** 2
            hp = self.ap - self.bp * (q / 2) ** 2
            n5_m3 = hm * self.m_pump * n_min + 2 * hp
            self.N5_M3.append(n5_m3)
            n6_m3 = hm * self.m_pump * self.n_max + 2 * hp
            self.N6_M3.append(n6_m3)
            n6_m2 = hm * (self.m_pump - 1) * self.n_max + 2 * hp
            self.N6_M2.append(n6_m2)
            w = 4 * q / (3600 * math.pi * (self.Dvn * 10 ** (-3)) ** 2)
            Re = w * self.Dvn * 10 ** (-3) / (self.vis_t * 10 ** (-6))
            if Re < 2300:
                lambda_ = 64 / Re
            elif 2300 < Re < self.Re1:
                lambda_ = 0.3164 / (Re ** 0.25)
            elif self.Re1 < Re < self.Re2:
                lambda_ = 0.11 * (68 / Re + self.k_) ** 0.25
            else:
                lambda_ = 0.11 * self.k_ ** 0.25
            ht = (lambda_ * (self.L * 10 ** 3 * w ** 2)) / (self.Dvn * 10 ** (-3) * 2 * self.G)
            hs = 1.02 * ht + self.delta_z + self.N_a * self.h_ost
            self.Hs.append(hs)
            i = ht / (self.L * 10 ** 3)
            hl = 1.02 * i * (self.L * 10 ** 3 - l_l * (1 - kaf_w)) + self.delta_z + self.N_a * self.h_ost
            self.Hs_with_looping.append(hl)

        all_h = [self.N5_M3, self.N6_M3, self.N6_M2, self.Hs, self.Hs_with_looping]
        labels = [f'n{n_min} m3', f'n{self.n_max} m3', f'n{self.n_max} m2', 'С постоянным диаметром', 'С лупингом']

        m_max = self.m_pump
        m_min = self.m_pump - 1
        async_result = pool.apply_async(self.check_transfer_mode, (self.Q_hour, self.n_max, m_min, self.H, 0.001))
        self.Q2, H2 = self.check_transfer_mode(self.Q_hour, self.n_max, m_max, self.H, 0.001)
        time.sleep(3)
        self.Q1, H1 = async_result.get()
        tau1 = 24 * self.Np * (self.Q2 - self.Q_hour) / (self.Q2 - self.Q1)

        tau2 = 24 * self.Np * (self.Q_hour - self.Q1) / (self.Q2 - self.Q1)
        hm = self.a_m - self.b_m * self.Q2 ** 2
        H_n_max_m_pump = hm * self.m_pump
        n_nps_first_section = math.ceil(self.n_max / self.N_a)
        list_with_value = [['delta', delta_n], ['Dvn', self.Dvn], ['Re1', self.Re1], ['Re2', self.Re2],
                           ['Re', self.Re], ['h_tr', self.h_t], ['i', self.i], ['H', self.H], ['n0', n0],
                           ['n_min', n_min], ['n_max', self.n_max], ['Q2', self.Q2], ['Q1', self.Q1],
                           ['H_n_max_m_pump', H_n_max_m_pump], ['n_nps_first_section', n_nps_first_section],
                           ['tau1', tau1], ['tau2', tau2], ['list_all_h', all_h], ['list_labels', labels],
                           ['q_list', self.q_list]]

        for name, value in list_with_value:
            self.dict_value[name] = value
        update_dict_to_db(self.dict_value, self.var)

    def calculate_H_Htr(self, Q, n, m_np):
        hm = self.a_m - self.b_m * Q ** 2
        hp = self.ap - self.bp * (Q / 2) ** 2
        Hst = hm * m_np
        H = Hst * n + self.N_a * hp
        w = 4 * Q / (3600 * np.pi * (self.Dvn * 10 ** (-3)) ** 2)
        Re = w * self.Dvn * 10 ** (-3) / (self.vis_t * 10 ** (-6))
        if Re < 2300:
            lambda_ = 64 / Re
        elif 2300 < Re < self.Re1:
            lambda_ = 0.3164 / (Re ** 0.25)
        elif self.Re1 < Re < self.Re2:
            lambda_ = 0.11 * (68 / Re + self.k_) ** 0.25
        else:
            lambda_ = 0.11 * self.k_ ** 0.25
        h_t = lambda_ * (self.L * 10 ** 3 * w ** 2) / (self.Dvn * 10 ** (-3) * 2 * self.G)
        H_tr = 1.02 * h_t + self.delta_z + self.N_a * self.h_ost
        H = Decimal(f'{H}')
        H = H.quantize(Decimal('1.000'), ROUND_HALF_UP)
        H_tr = Decimal(f'{H_tr}')
        H_tr = H_tr.quantize(Decimal('1.000'), ROUND_HALF_UP)
        return H, H_tr

    def check_transfer_mode(self, Q, n, m_np, H_tr, num):
        if 0 + num > 0:
            Q += 200
        else:
            Q -= 200
        hm = self.a_m - self.b_m * Q ** 2
        hp = self.ap - self.bp * (Q / 2) ** 2
        Hst = hm * m_np
        H = Hst * n + hp * self.N_a
        while H != H_tr:
            if H > H_tr:
                while H > H_tr:
                    Q = Q + num
                    H, H_tr = self.calculate_H_Htr(Q, n, m_np)
            else:
                while H_tr > H:
                    Q = Q - num
                    H, H_tr = self.calculate_H_Htr(Q, n, m_np)
            H = H.quantize(Decimal('1.00'), ROUND_HALF_UP)
            H_tr = H_tr.quantize(Decimal('1.00'), ROUND_HALF_UP)
        else:
            return Q, H

    def calculate_fourth_part(self):
        # Данные для растановки НПС
        self.dict_value = get_source_dict(self.var)
        hm = self.a_m - self.b_m * self.Q2 ** 2
        hp = self.ap - self.bp * (self.Q2 / 2) ** 2
        Hst = hm * self.m_pump
        w = 4 * self.Q2 / (3600 * math.pi * (self.Dvn * 10 ** (-3)) ** 2)
        Re = w * self.Dvn * 10 ** (-3) / (self.vis_t * 10 ** (-6))
        H_for_calc_delta = Hst + hp - self.h_ost
        if Re < 2300:
            lambda_ = 64 / Re
        elif 2300 < Re < self.Re1:
            lambda_ = 0.3164 / (Re ** 0.25)
        elif self.Re1 < Re < self.Re2:
            lambda_ = 0.11 * (68 / Re + self.k_) ** 0.25
        else:
            lambda_ = 0.11 * self.k_ ** 0.25
        # Потери напора на трение
        h_t = lambda_ * (self.L * 10 ** 3 * w ** 2) / (self.Dvn * 10 ** (-3) * 2 * self.G)
        # Гидравлический уклон
        i_2 = h_t / (self.L * 10 ** 3)
        first_kat = 100
        second_kat = 1.02 * i_2 * first_kat * 1000
        tag = first_kat / second_kat
        coordinates = get_list_coordinates(self.var)
        zes, xes = [], []
        for x, y in coordinates:
            xes.append(x)
            zes.append(y)
        list_with_coordinates_for_drawing, list_with_coordinates_nps, list_index_main_nps = self.calculate_draw_coordinates(
            hp, Hst, tag,
            xes, zes)

        list_with_value = [['list_coordinates_for_drawing', list_with_coordinates_for_drawing],
                           ['list_coordinates_nps', list_with_coordinates_nps],
                           ['H_for_calc_delta', H_for_calc_delta],
                           ['list_index_main_nps', list_index_main_nps],
                           ['second_kat', second_kat]]

        for name, value in list_with_value:
            self.dict_value[name] = value
        update_dict_to_db(self.dict_value, self.var)

    def calculate_draw_coordinates(self, hp, Hst, tag, xes, zes):
        list_with_coordinates_for_drawing = []
        list_with_coordinates_nps = []

        p1 = [xes[0], zes[0]]
        p2 = [xes[-1], zes[0]]
        list_with_coordinates_for_drawing.append([p1, p2])
        p1 = [xes[-1], zes[0]]
        p2 = [xes[-1], zes[-1]]
        list_with_coordinates_for_drawing.append([p1, p2])

        for i, x in enumerate(xes):
            if x == xes[-1]:
                break
            p1 = [x, zes[i]]
            p2 = [xes[i + 1], zes[i + 1]]
            list_with_coordinates_for_drawing.append([p1, p2])

        def calculate_index(x1_1, y1_1, x1_2, y1_2, x2_1, y2_1, x2_2, y2_2):
            A1 = y1_1 - y1_2
            B1 = x1_2 - x1_1
            C1 = x1_1 * y1_2 - x1_2 * y1_1
            A2 = y2_1 - y2_2
            B2 = x2_2 - x2_1
            C2 = x2_1 * y2_2 - x2_2 * y2_1
            if B1 * A2 - B2 * A1 != 0:
                y = (C2 * A1 - C1 * A2) / (B1 * A2 - B2 * A1)
                if A1 == 0:
                    x = (-C2 - B2 * y) / A2
                elif A2 == 0:
                    x = (-C1 - B1 * y) / A1
                else:
                    x = (-C2 - B2 * y) / A2
                # проверяем, находится ли решение системы (точка пересечения) на первом отрезке, min/max - потому
                # что координаты точки могут быть заданы не по порядку возрастания
                if min(x2_1, x2_2) <= x <= max(x2_1, x2_2) and min(y2_1, y2_2) <= y <= max(y2_1, y2_2):
                    return x, y
                else:
                    return None
            # случай деления на ноль, то есть параллельность
            if B1 * A2 - B2 * A1 == 0:
                return None

        x1 = xes[0]
        z1 = zes[0]
        number = math.ceil(self.n_max / self.N_a)
        list_numbers_nps = [number + 1 for number in range(self.n_max)]
        list_index_main_nps = [0]
        for index, number_nps in enumerate(list_numbers_nps):
            if number_nps % number == 0 or number_nps == list_numbers_nps[-1] or number == 1:
                list_index_main_nps.append(index)
                p1 = [x1, z1]
                z2 = z1 + Hst + hp - self.h_ost
                p2 = [x1, z2]
                list_with_coordinates_nps.append(p1)
                list_with_coordinates_for_drawing.append([p1, p2])
                p1 = p2
                x1 += tag * (Hst + hp - self.h_ost)
                p1_hp_line = [p1[0], p1[1] + self.h_ost]
                for i, x2 in enumerate(xes):
                    if x2 == xes[-1]:
                        break
                    p = calculate_index(p1[0], p1[1], x1, z1, x2, zes[i], xes[i + 1], zes[i + 1])
                    if p is not None:
                        x1 = p[0]
                        z1 = p[1]
                        p2 = [x1, z1]
                        p2_hp_line = [p2[0], p2[1] + self.h_ost]
                        list_with_coordinates_for_drawing.append([p1, p2])
                        list_with_coordinates_for_drawing.append([p1_hp_line, p2_hp_line])
                        break
                    elif p is None and x2 == xes[-2]:
                        x1 = xes[-1]
                        z1 = zes[-1]
                        p2 = [x1, z1]
                        p2_hp_line = [p2[0], p2[1] + self.h_ost]
                        list_with_coordinates_for_drawing.append([p1, p2])
                        list_with_coordinates_for_drawing.append([p1_hp_line, p2_hp_line])

            else:
                p1 = [x1, z1]
                z2 = z1 + Hst
                p2 = [x1, z2]
                list_with_coordinates_nps.append(p1)
                list_with_coordinates_for_drawing.append([p1, p2])
                p1 = p2
                x1 += tag * Hst
                p1_hp_line = [p1[0], p1[1] + hp]
                for i, x2 in enumerate(xes):
                    if x2 == xes[-1]:
                        break
                    p = calculate_index(p1[0], p1[1], x1, z1, x2, zes[i], xes[i + 1], zes[i + 1])
                    if p is not None:
                        x1 = p[0]
                        z1 = p[1]
                        p2 = [x1, z1]
                        p2_hp_line = [p2[0], p2[1] + hp]
                        list_with_coordinates_for_drawing.append([p1, p2])
                        list_with_coordinates_for_drawing.append([p1_hp_line, p2_hp_line])
                        break
                    elif p is None and x2 == xes[-2]:
                        x1 = xes[-1]
                        z1 = zes[-1]
                        p2 = [x1, z1]
                        p2_hp_line = [p2[0], p2[1] + hp]
                        list_with_coordinates_for_drawing.append([p1, p2])
                        list_with_coordinates_for_drawing.append([p1_hp_line, p2_hp_line])
        return list_with_coordinates_for_drawing, list_with_coordinates_nps, list_index_main_nps


def draw_graph_in_calculate(var):
    dict_value = get_source_dict(var)
    for name, value in dict_value.items():
        if name == 'list_all_h':
            all_h = value
        elif name == 'list_labels':
            labels = value
        elif name == 'T_k':
            T_k = value
        elif name == 'vis_T':
            vis_T = value
        elif name == 'q_list':
            q_list = value
    plot_show(T_k, vis_T, 'T,K', 'mm2/s', 'Вискограмма')
    many_plot(q_list, all_h, 'Q, м3/x', 'Н,м', labels, 'Совмещенная характеристика', COLORS)
