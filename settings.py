# -*- coding: utf-8 -*-
"""
Created on Thu Oct  8 21:35:52 2020

@author: stinc
"""

from json import dumps, loads
from models import SourceDataTable, InformationDeltaTable, ModeInformationDeltaTable, CoordinatesTable, \
    CheckInformationDeltaTable, OptionStateTable, ActionVarTable, MainPumpsTable, SupportPumpsTable, PipeTable, \
    DataOddsTable
import re

LIST_NAME_DATA_TABLE7 = ['finish_data_list', 'list_with_data_category']
LIST_DELETE = [SourceDataTable, CoordinatesTable, InformationDeltaTable, ModeInformationDeltaTable, ActionVarTable,
               CheckInformationDeltaTable, OptionStateTable]
LIST_UPDATE = [SourceDataTable, CoordinatesTable, InformationDeltaTable, ModeInformationDeltaTable,
               CheckInformationDeltaTable, OptionStateTable]

LIST_WITH_NAME_VALUE_CHARACTIRISTIES = ['L', 'section_length', 'operating_pressure', 'Gg', 'knp', 'Tr', 'h_ost',
                                        'm_pump', 'Np']
LIST_WITH_NAME_VALUE_OIL_PROPERTIES = ['density', 'vis_1', 'vis_2', 'T1', 'T2']
LIST_WITH_VALUE = ['density_t', 'vis_t', 'Q_hour', 'brand_pump_m', 'd_work_m', 'brand_pump_s', 'd_work_s', 'Dn',
                   'delta', 'Dvn', 'Re1', 'Re2', 'Re', 'h_tr', 'i', 'H', 'n0', 'n_max', 'n_min', 'Q2', 'Q1',
                   'H_n_max_m_pump', 'tau1', 'tau2']
LIST_WITH_NAME = ['Расчётная плотность, кг/м\u00B3', 'Расчётная вязкость, мм/с\u00B2',
                  'Часовая производительность, м\u00B3/ч',
                  'Марка магистрального насоса', 'Диаметр рабочего колеса магистрального насоса',
                  'Марка подпорного насоса', 'Диаметр рабочего колеса подпорного насоса',
                  'Наружный диаметр, мм',
                  'Толщина стенки, мм', 'Внутренний диаметр, мм', 'Re\u2081', 'Re\u2082', 'Re', 'Потери на трение, м',
                  'Гидравлический уклон', 'Полные потери на трение, м', 'Расчётное количество станций',
                  'Станций при округлении в большую сторону', 'Станций при округлении в меньшую сторону',
                  'Расход при {n_max} станций и {m_pump} насосов, м\u00B3/ч',
                  'Расход при {n_max} станций и {m_pump} насосов, м\u00B3/ч',
                  'Напор станции при {n_max} станций и {m_pump} насосов, м',
                  'Время работы с {n_max} НПС', 'Время работы с {n_max} НПС']

FIRST_NAME_ACTION_VAR = 'action_var_1'
FIRST_NAME_VAR = 'Новый'

LIST_WITH_TABLE_VALUE_CALC_7 = [
    ['Внутренний диаметр, мм', 'Толщина стенки трубы, мм', 'Временное сопротивление стали, МПа',
     'Коэффициент надежности по материалу, k\u2081', 'Коэффициентов надежности по нагрузке, np',
     'Коэффициент надежности по назначению, kн',
     'Коэффициент условий работы, m', 'Плотность, м\u00B3/кг', 'Напор станции, м'],
    ['Dvn', 'delta', 'R1n', 'k1', 'np', 'kn', 'm_kaf', 'density_t', 'H_for_calc_delta']]

LIST_WITH_NAME_SOURCE_VALUE_8 = ['h_min', 'a_']
SUP = str.maketrans('nom', '\u2099\u2092\u2098')
SUP_2 = str.maketrans('max', '\u2098\u2090\u2093')
SUP_3 = str.maketrans('ps', '\u209A\u209B')
NUMBER_LOW_INDEX = str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉")

re_data = re.compile(r'[0-9]*[.,]?[0-9]+')
HELP = 'Добавте строку и внесите новые данные или измените имеющиеся и нажмите кнопку "Внести изменения".'


def check_data(string):
    match = re.fullmatch(re_data, string)
    if match:
        return True
    else:
        return None


def get_source_dict(var):
    source_data = SourceDataTable.get_or_none(SourceDataTable.var == var)
    if source_data is None:
        return None
    dict_value = loads(source_data.json_data)
    return dict_value


def update_dict_to_db(dict_value, var):
    json_data = dumps(dict_value)
    source = (
        SourceDataTable.update({SourceDataTable.json_data: json_data})).where(
        SourceDataTable.var == var)
    source.execute()


def get_list_coordinates(var):
    source = CoordinatesTable.select().where(CoordinatesTable.var == var).get()
    json_coordinates = source.json_coordinates
    coordinates = loads(json_coordinates)
    return coordinates


def update_list_coordinates_to_db(list_coordinates, var):
    json_data = dumps(list_coordinates)
    source = (
        CoordinatesTable.update({CoordinatesTable.json_coordinates: json_data})).where(
        CoordinatesTable.var == var)
    source.execute()


def create_new_data_var_5(var, list_with_coordinates, dict_with_value):
    json_coordinates = dumps(list_with_coordinates)
    coordinates = CoordinatesTable(var=var, json_coordinates=json_coordinates)
    coordinates.save()
    json_source_data = dumps(dict_with_value)
    source = SourceDataTable(var=var, json_data=json_source_data)
    source.save()


def check_update_data_var_7(var, name_value, list_with_data):
    info = InformationDeltaTable.get_or_none(
        InformationDeltaTable.var == var)
    if info is None:
        dict_values = {name_value: list_with_data}
        json_data = dumps(dict_values)
        data_category = InformationDeltaTable(var=var, json_data=json_data)
        data_category.save()
    else:
        json_data = info.json_data
        dict_values = loads(json_data)
        dict_values[name_value] = list_with_data
        json_data = dumps(dict_values)
        info = (
            InformationDeltaTable.update({InformationDeltaTable.json_data: json_data})).where(
            InformationDeltaTable.var == var)
        info.execute()


def get_info_table_list(var, name_value):
    info_section = InformationDeltaTable.get_or_none(InformationDeltaTable.var == var)
    if info_section is None:
        return None
    json_data = info_section.json_data
    dict_values = loads(json_data)
    if name_value not in dict_values.keys():
        return None
    list_with_data = dict_values[name_value]
    return list_with_data


def get_table_list_8(var):
    info_table = ModeInformationDeltaTable.get_or_none(ModeInformationDeltaTable.var == var)
    if info_table is None:
        return None
    json_data = info_table.json_data
    table_list = loads(json_data)
    return table_list


def check_update_table_list_8_to_db(table_list, var):
    info_table_8 = ModeInformationDeltaTable.get_or_none(
        ModeInformationDeltaTable.var == var)
    json_data = dumps(table_list)
    if info_table_8 is None:
        data_category = ModeInformationDeltaTable(var=var, json_data=json_data)
        data_category.save()
    else:
        info_table_8 = (
            ModeInformationDeltaTable.update({ModeInformationDeltaTable.json_data: json_data})).where(
            ModeInformationDeltaTable.var == var)
        info_table_8.execute()


def delete_data_7_8(var, mode):
    """Два режима использования функции: 1 - удалем данные из 3(8) модуля; 2 - удаляем из 2(7) и 3(8) модуля."""
    source = ModeInformationDeltaTable.get_or_none(ModeInformationDeltaTable.var == var)
    if source is not None:
        source = ModeInformationDeltaTable.delete().where(ModeInformationDeltaTable.var == var)
        source.execute()
    source = CheckInformationDeltaTable.get_or_none(CheckInformationDeltaTable.var == var)
    if source is not None:
        source = CheckInformationDeltaTable.delete().where(CheckInformationDeltaTable.var == var)
        source.execute()
    if mode == 2:
        info_section = InformationDeltaTable.get_or_none(InformationDeltaTable.var == var)
        if info_section is not None:
            info_section = InformationDeltaTable.delete().where(InformationDeltaTable.var == var)
            info_section.execute()


def load_list_data_to_check_table(list_late_data, var):
    source = CheckInformationDeltaTable.get_or_none(CheckInformationDeltaTable.var == var)
    json_data = dumps(list_late_data)
    if source is None:
        source = CheckInformationDeltaTable(var=var, json_data=json_data)
        source.save()
        return


def check_list_late_source_data_8(var, name_list_hmax, name_list_lenth):
    source = CheckInformationDeltaTable.get_or_none(CheckInformationDeltaTable.var == var)
    if source is None:
        return True
    json_data = source.json_data
    list_late_data = loads(json_data)
    finish_data_7 = get_info_table_list(var, name_list_hmax)
    list_category_data = get_info_table_list(var, name_list_lenth)
    list_hmax = [list_7[3] for list_7 in finish_data_7]
    list_lenth_section = [lenth for lenth in list_category_data[1]]
    if list_late_data[1] == list_hmax and list_late_data[0] == list_lenth_section:
        return True
    else:
        return False


def find_var(table, var):
    source = table.get_or_none(table.var == var)
    if source is not None:
        return True


def delete_func(var):
    for table in LIST_DELETE:
        if find_var(table, var) is True:
            source = table.delete().where(table.var == var)
            source.execute()


def load_update_var_state(var, state):
    source = OptionStateTable.get_or_none(
        OptionStateTable.var == var)
    if source is None:
        source = OptionStateTable(var=var, option=state)
        source.save()
    else:
        source = (
            OptionStateTable.update({OptionStateTable.option: state})).where(
            OptionStateTable.var == var)
        source.execute()


def get_state_var(var):
    source_data = OptionStateTable.select().where(OptionStateTable.var == var).get()
    return source_data.option


def get_list_main_pumps():
    list_with_pumps = []
    for info in MainPumpsTable.select():
        list_with_pumps.append([info.brand, info.rotor, info.impeller_diameter,
                                info.a, info.b, info.Q_nom, info.kaf])
    list_with_pumps.sort(key=lambda k: k[5])
    return list_with_pumps


def get_list_sup_pumps():
    list_with_pumps = []
    for info in SupportPumpsTable.select():
        list_with_pumps.append([info.brand, info.impeller_diameter,
                                info.a, info.b, info.Q_nom])
    list_with_pumps.sort(key=lambda k: k[4])
    return list_with_pumps


def get_list_pipe():
    list_with_pipes = []
    for info in PipeTable.select():
        list_with_pipes.append([info.brand, info.diameter,
                                info.R1n, info.k1])
    list_with_pipes.sort(key=lambda k: k[1])
    return list_with_pipes


def update_var_table(last_var, new_var):
    for table in LIST_UPDATE:
        if find_var(table, last_var) is True:
            source = (table.update({table.var: new_var})).where(table.var == last_var)
            source.execute()


def get_value_kaf(index):
    data = DataOddsTable.get_or_none(DataOddsTable.id == index)
    if data is None:
        return ''
    value = str(data.value)
    return value


def update_(last_var, new_var):
    for table in LIST_UPDATE:
        if find_var(table, last_var) is True:
            source = (table.update({table.var: new_var})).where(table.var == last_var)
            source.execute()
