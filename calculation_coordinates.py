# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 21:35:52 2020

@author: stinc
"""
# from calculate_5 import hp, hm, Hst, tag, zes, xes, N_a, n_max, h_ost
from decimal import getcontext
hp = 87.28510500450601
Hst = 573.8063148549916
tag = 0.3507248563742432
zes = [106.0, 126.5, 131.4, 140.0, 154.0, 150.0, 163.0, 175.0, 170.0, 184.0, 187.0]
xes = [0.0, 100.0, 200.0, 300.0, 400.0, 500.0, 600.0, 700.0, 800.0, 900.0, 1011.0]
N_a = 2
n_max = 5
h_ost = 40.0
getcontext().prec = 50
list_with_coordinates_for_drawing = []
list_with_coordinates_nps = []

p1 = [xes[0], zes[0]]
p2 = [xes[-1], zes[0]]
list_with_coordinates_for_drawing.append([p1, p2])
p1 = [xes[0], zes[0]]
p2 = [xes[0], zes[-1] + 200]
list_with_coordinates_for_drawing.append([p1, p2])
p1 = [xes[-1], zes[0]]
p2 = [xes[-1], zes[-1]]
list_with_coordinates_for_drawing.append([p1, p2])

try:
    for i, x in enumerate(xes):
        if x == xes[-1]:
            break
        p1 = [x, zes[i]]
        p2 = [xes[i + 1], zes[i + 1]]
        list_with_coordinates_for_drawing.append([p1, p2])
except Exception as exc:
    print(exc)


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


try:
    x1 = xes[0]
    z1 = zes[0]
    z2 = 0
    number = round(n_max / N_a)
    for index, number_nps in enumerate(range(n_max)):
        if (index + 1) % number == 0 or index == -1:
            p1 = [x1, z1]
            z2 = z1 + Hst + hp - h_ost
            p2 = [x1, z2]
            list_with_coordinates_nps.append(p1)
            list_with_coordinates_for_drawing.append([p1, p2])
            p1 = p2
            x1 += tag * (Hst + hp - h_ost)
            for i, x2 in enumerate(xes):
                if x2 == xes[-1]:
                    break
                p = calculate_index(p1[0], p1[1], x1, z1, x2, zes[i], xes[i + 1], zes[i + 1])
                if p is not None:
                    x1 = p[0]
                    z1 = p[1]
                    p2 = [x1, z1]
                    list_with_coordinates_for_drawing.append([p1, p2])
                    break

        else:
            p1 = [x1, z1]
            z2 = z1 + Hst
            p2 = [x1, z2]
            list_with_coordinates_nps.append(p1)
            list_with_coordinates_for_drawing.append([p1, p2])
            p1 = p2
            x1 += tag * Hst
            for i, x2 in enumerate(xes):
                if x2 == xes[-1]:
                    break
                p = calculate_index(p1[0], p1[1], x1, z1, x2, zes[i], xes[i + 1], zes[i + 1])
                if p is not None:
                    x1 = p[0]
                    z1 = p[1]
                    p2 = [x1, z1]
                    list_with_coordinates_for_drawing.append([p1, p2])
                    break
except Exception as exc:
    print(exc)

print(list_with_coordinates_for_drawing)
