# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 21:35:52 2020

@author: stinc
"""
import math

from pyautocad import Autocad, APoint
import matplotlib.pyplot as plt

LINE_ELSE = 170
ANGLE = 1.57


def draw_line(p1, p2, acad):
    p1 = APoint(p1[0], p1[1])
    p2 = APoint(p2[0], p2[1])
    acad.model.AddLine(p1, p2)


def add_text(p, acad, size, text):
    p = APoint(p[0], p[1])
    acad.model.AddText(text, p, size)


def drawing_autocad(list_with_coordinates_for_drawing, list_coordinates_nps, H_for_calc_delta, list_index_main_nps, L,
                    delta_z, second_kat):
    acad = Autocad(create_if_not_exists=True)
    H_plus = H_for_calc_delta + LINE_ELSE

    for p1, p2 in list_with_coordinates_for_drawing:
        p1 = APoint(p1[0], p1[1])
        p2 = APoint(p2[0], p2[1])
        acad.model.AddLine(p1, p2)

    for index, p1 in enumerate(list_coordinates_nps):
        if index == 0:
            z_finish = p1[1] + delta_z
            x_start = p1[0]
            z_start = p1[1]
        p1 = APoint(p1[0], p1[1])
        p2 = [p1[0], (p1[1] + H_plus)]
        p2 = APoint(p2[0], p2[1])
        acad.model.AddLine(p1, p2)
        p1 = [p1[0], (p1[1] + H_plus)]
        p1 = APoint(p1[0], p1[1])
        acad.model.AddCircle(p1, 50)
        acad.model.AddCircle(p1, 30)
        p2 = [p1[0] + 50, p1[1]]
        p2 = APoint(p2[0], p2[1])
        acad.model.AddLine(p1, p2)
        p2 = [p1[0] - 50, p1[1]]
        p2 = APoint(p2[0], p2[1])
        acad.model.AddLine(p1, p2)
        p2 = [p1[0], p1[1] + 50]
        p2 = APoint(p2[0], p2[1])
        acad.model.AddLine(p1, p2)
        p_draw_text = [p2.x - 30, p2.y + 30]
        add_text(p_draw_text, acad, 30, f'ПС {index + 1}')
        p2 = [p1[0], p1[1] - 50]
        p2 = APoint(p2[0], p2[1])
        acad.model.AddLine(p1, p2)
        p1 = [p1.x, p1.y - 80]
        p2 = [p1[0] + 40, p1[1]]
        draw_line(p1, p2, acad)
        if index in list_index_main_nps:
            size_base = 70
        else:
            size_base = 50
        p1 = [p2[0], p2[1]]
        p2 = [p1[0], p1[1] - size_base / 2]
        draw_line(p1, p2, acad)
        p1 = [p2[0], p2[1]]
        p2 = [p1[0] + size_base, p1[1]]
        draw_line(p1, p2, acad)
        p1 = [p2[0], p2[1]]
        p2 = [p1[0], p1[1] + size_base / 2]
        draw_line(p1, p2, acad)
        p1 = [p2[0], p2[1]]
        p2 = [p1[0] - size_base, p1[1]]
        draw_line(p1, p2, acad)
        p1 = [p2[0], p2[1]]
        p2 = [p1[0] + size_base / 2, p1[1] + size_base / 2]
        draw_line(p1, p2, acad)
        p1 = [p2[0], p2[1]]
        p2 = [p1[0] + size_base / 2, p1[1] - size_base / 2]
        draw_line(p1, p2, acad)
    else:
        p1 = [L, z_finish]
        p2 = [p1[0], z_finish + H_plus]
        draw_line(p1, p2, acad)
        p1 = p2
        p2 = [p1[0] + 35, p1[1]]
        draw_line(p1, p2, acad)
        p1 = p2
        p2 = [p1[0], p1[1] + 70]
        draw_line(p1, p2, acad)
        p_draw_text = [p2[0] - 65, p2[1] + 30]
        add_text(p_draw_text, acad, 30, f'КП')
        p1 = p2
        p2 = [p1[0] - 70, p1[1]]
        draw_line(p1, p2, acad)
        p1 = p2
        p2 = [p1[0], p1[1] - 70]
        draw_line(p1, p2, acad)
        p1 = p2
        p2 = [p1[0] + 35, p1[1]]
        draw_line(p1, p2, acad)
        p1 = p2
        p2 = [p1[0], p1[1] + 35]
        draw_line(p1, p2, acad)
        p1 = p2
        p2 = [p1[0] + 35, p1[1]]
        draw_line(p1, p2, acad)
        p2 = [p1[0] - 35, p1[1]]
        draw_line(p1, p2, acad)
        p2 = [p1[0], p1[1] + 35]
        draw_line(p1, p2, acad)
    z_start = math.ceil(z_start)
    z_start_H_plus = math.ceil(z_start + H_plus + 50)
    x_start -= 200
    x_start = math.ceil(x_start)
    p1 = [x_start, z_start]
    for z in range(z_start, z_start_H_plus, 50):
        p2 = [x_start, z]
        draw_line(p1, p2, acad)
        p3 = [x_start + 40, z]
        draw_line(p2, p3, acad)
        p3 = [x_start + 50, z]
        add_text(p3, acad, 20, f'{z} м')
        p1 = p2
    x_start += 200
    z_start -= 155
    p1 = [x_start, z_start]
    x_finish = math.ceil(L + 50)
    for x in range(x_start, x_finish, 50):
        p2 = [x, z_start]
        draw_line(p1, p2, acad)
        p3 = [x, z_start + 40]
        draw_line(p2, p3, acad)
        p3 = [x + 5, z_start + 50]
        add_text(p3, acad, 20, f'{x} км')
        p1 = p2
    p1 = [p1[0] + 50, p1[1] + H_plus]
    p2 = [p1[0], p1[1] + second_kat]
    draw_line(p1, p2, acad)
    p3 = [p1[0] + 100, p1[1]]
    draw_line(p1, p3, acad)
    draw_line(p2, p3, acad)
    p2 = [p1[0], p1[1] - 30]
    p1 = [p1[0] - 10, p1[1]]
    add_text(p1, acad, 20, f'1,02 * i * l = {second_kat} м')
    add_text(p2, acad, 20, f'l = 100 км')
    for text in acad.iter_objects_fast('Text'):
        if 'км' in text.TextString and 'l' not in text.TextString:
            text.Rotation = ANGLE
        elif 'i' in text.TextString:
            text.Rotation = ANGLE


def drawing_plt(list_for_drawing):
    plt.figure()
    for p1, p2 in list_for_drawing:
        x = [p1[0], p2[0]]
        y = [p1[1], p2[1]]
        plt.plot(x, y)
    plt.show()
