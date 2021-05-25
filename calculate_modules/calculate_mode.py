# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 21:35:52 2020

@author: stinc
"""

import itertools


def func_remove_place(comb, index, amount_pump):
    comb[index] = amount_pump
    return comb


def calculate_mode_transportation(number_nps, number_pump):
    # number_nps: int, number_pump: string
    comb = number_nps * [number_pump]
    list_with_amount_pumps = [num for num in range(int(number_pump))]
    list_with_amount_pumps.reverse()
    list_res = []
    for i in range(int(number_pump)):
        for num in list_with_amount_pumps:
            for index, n in enumerate(range(number_nps)):
                for combination in itertools.permutations(comb, number_nps):
                    if combination in list_res:
                        continue
                    list_res.append(combination)
                if index == len(range(number_nps)) - 1:
                    continue
                comb = func_remove_place(comb, index, str(num))
        number_pump_for_calc = int(number_pump) - (i + 1)
        comb = number_nps * [f'{number_pump_for_calc}']

    list_finish_res = []
    for index, comb in enumerate(list_res):
        if int(comb[0]) != 0:
            list_finish_res.append(comb)

    return list_finish_res
