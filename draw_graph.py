# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 21:35:52 2020

@author: stinc
"""
from pyautocad import Autocad, APoint
import matplotlib.pyplot as plt


def drawing_autocad(list_with_coordinates_for_drawing):
    acad = Autocad(create_if_not_exists=True)

    for p1, p2 in list_with_coordinates_for_drawing:
        p1 = APoint(p1[0], p1[1])
        p2 = APoint(p2[0], p2[1])
        acad.model.AddLine(p1, p2)


def drawing_plt(list_for_drawing):
    plt.figure()
    for p1, p2 in list_for_drawing:
        x = [p1[0], p2[0]]
        y = [p1[1], p2[1]]
        plt.plot(x, y, marker='o')
    plt.show()
