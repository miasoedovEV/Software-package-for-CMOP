import peewee
import os
import pandas as pd
import numpy as np
import json

FILE_NAME_XLS = 'source_data.xlsx'
NAME_DATA_BASE = 'source_data.db'


class CreatorDataBase:

    def __init__(self, file_name, db_name):
        self.file_name = file_name
        self.db_name = db_name

    def load_data(self):
        file_source_data = self.file_name
        # Load spreadsheet
        xl_source_data = pd.ExcelFile(file_source_data)
        df_graph_speed = xl_source_data.parse('graph_speed')
        array_graph_speed = np.array(pd.DataFrame(df_graph_speed))  # Масив с данными для графика скорости
        self.Q_graph = list(array_graph_speed[:, 0])
        self.w0_graph = list(array_graph_speed[:, 1])
        df_data_Dn = xl_source_data.parse('data_Dn')
        array_data_Dn = np.array(pd.DataFrame(df_data_Dn))  # Масив с данными о таблице диаметров
        self.Dn_list = list(array_data_Dn[:, 2])
        df_source_data = xl_source_data.parse('data of main pumps')
        array_data_main_pumps = np.array(pd.DataFrame(df_source_data))  # Масив со списком насосов
        self.list_with_main_pumps = array_data_main_pumps.tolist()
        self.list_with_main_pumps.sort(key=lambda k: k[5])
        df_source_data = xl_source_data.parse('data of support pumps')
        array_data_suport_pumps = np.array(pd.DataFrame(df_source_data))  # Масив со списком подпорных насосов
        self.list_with_suport_pumps = array_data_suport_pumps.tolist()
        self.list_with_suport_pumps.sort(key=lambda k: k[4])
        df_source_data = xl_source_data.parse('coefficients')
        array_data_coefficients = np.array(pd.DataFrame(df_source_data))  # Масив со списком подпорных насосов

        self.database = peewee.SqliteDatabase('source_data.db')
        self.dict_data_infor_kaf = {}
        for index, kaf in enumerate(array_data_coefficients[:, 0]):
            if kaf != kaf or array_data_coefficients[:, 1][index] != array_data_coefficients[:, 1][index] or \
                    array_data_coefficients[:, 2][index] != array_data_coefficients[:, 2][index]:
                continue
            if kaf not in self.dict_data_infor_kaf.keys():
                self.dict_data_infor_kaf[kaf] = [
                    [array_data_coefficients[:, 1][index], array_data_coefficients[:, 2][index]]]
            else:
                self.dict_data_infor_kaf[kaf].append(
                    [array_data_coefficients[:, 1][index], array_data_coefficients[:, 2][index]])

    def create_data_base(self):
        self.database = peewee.SqliteDatabase(self.db_name)

        class BaseTable(peewee.Model):
            # В подклассе Meta указываем подключение к той или иной базе данных
            class Meta:
                database = self.database

        # Чтобы создать таблицу в нашей БД, нам нужно создать класс
        class GraphW0(BaseTable):
            json_w0 = peewee.CharField()
            json_Q = peewee.CharField()  # от типа столбца зависит тип данных, который мы сможем в него записать

        class DnTable(BaseTable):
            json_dn = peewee.CharField()

        class MainPumpsTable(BaseTable):
            brand = peewee.CharField()
            rotor = peewee.CharField()
            impeller_diameter = peewee.CharField()
            a = peewee.FloatField()
            b = peewee.FloatField()
            Q_nom = peewee.FloatField()
            kaf = peewee.FloatField()

        class SupportPumpsTable(BaseTable):
            brand = peewee.CharField()
            impeller_diameter = peewee.CharField()
            a = peewee.FloatField()
            b = peewee.FloatField()
            Q_nom = peewee.FloatField()

        class CoordinatesTable(BaseTable):
            var = peewee.CharField()
            json_coordinates = peewee.CharField()

        class SourceDataTable(BaseTable):
            var = peewee.CharField()
            json_data = peewee.CharField()

        class ActionVarTable(BaseTable):
            var = peewee.CharField()

        class InformationDeltaTable(BaseTable):
            var = peewee.CharField()
            json_data = peewee.CharField()

        class ModeInformationDeltaTable(BaseTable):
            var = peewee.CharField()
            json_data = peewee.CharField()

        class CheckInformationDeltaTable(BaseTable):
            var = peewee.CharField()
            json_data = peewee.CharField()

        class OptionStateTable(BaseTable):
            var = peewee.CharField()
            option = peewee.IntegerField()

        class PipeTable(BaseTable):
            brand = peewee.CharField()
            diameter = peewee.FloatField()
            R1n = peewee.FloatField()
            k1 = peewee.FloatField()

        class DataOddsTable(BaseTable):
            name = peewee.CharField()
            cause = peewee.CharField()
            value = peewee.FloatField()

        self.database.create_tables([GraphW0, DnTable, MainPumpsTable, SupportPumpsTable,
                                     CoordinatesTable, SourceDataTable,
                                     ActionVarTable, InformationDeltaTable, ModeInformationDeltaTable,
                                     CheckInformationDeltaTable, OptionStateTable, PipeTable, DataOddsTable])

        # # Запись данных в таблицы:
        # # Один способ с явным save()
        graph = GraphW0(json_w0=json.dumps(self.w0_graph), json_Q=json.dumps(self.Q_graph))
        graph.save()

        Dn = DnTable(json_dn=json.dumps(self.Dn_list))
        Dn.save()

        for brand, rotor, impeller_diameter, a, b, Qnom, kaf in self.list_with_main_pumps:
            if brand != brand or rotor != rotor or impeller_diameter != impeller_diameter or a != a or b != b or Qnom != Qnom or kaf != kaf:
                continue
            main_pump = MainPumpsTable(
                brand=brand,
                rotor=rotor,
                impeller_diameter=impeller_diameter,
                a=a,
                b=b,
                Q_nom=Qnom,
                kaf=kaf
            )
            main_pump.save()

        for brand, impeller_diameter, a, b, Qnom in self.list_with_suport_pumps:
            if brand != brand or impeller_diameter != impeller_diameter or a != a or b != b or Qnom != Qnom:
                continue
            main_pump = SupportPumpsTable(
                brand=brand,
                impeller_diameter=impeller_diameter,
                a=a,
                b=b,
                Q_nom=Qnom
            )
            main_pump.save()
        for key, list_with_data in self.dict_data_infor_kaf.items():
            for cause, value in list_with_data:
                data = DataOddsTable(
                    name=key,
                    cause=cause,
                    value=value
                )
                data.save()

    def run(self):
        self.load_data()
        self.create_data_base()


if not os.path.exists(NAME_DATA_BASE):
    creator_data_base = CreatorDataBase(FILE_NAME_XLS, NAME_DATA_BASE)
    creator_data_base.run()
