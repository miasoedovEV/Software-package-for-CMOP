import csv

import peewee
import os
import json

FILE_NAME_GRAPH_SPEED = 'graph_speed.csv'
FILE_NAME_DATA_DN = 'data_Dn.csv'
FILE_DATA_MAIN_PUMPS = 'data_main_pumps.csv'
FILE_DATA_SUPPORT_PUMPS = 'data_support_pumps.csv'
FILE_DATA_COEFFICIENTS = 'coefficients.csv'
NAME_DATA_BASE = 'source_data.db'


def check_comma(value):
    if type(value) is str and ',' in value:
        value = value.replace(',', '.')
    return value


class CreatorDataBase:

    def __init__(self, db_name):
        self.db_name = db_name

    def load_data(self):
        self.Q_graph = []
        self.w0_graph = []
        with open(FILE_NAME_GRAPH_SPEED, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')  # <csv.DictReader object at 0x03B11030>
            for row in reader:
                Q = row['Q']
                w = row['v']
                self.Q_graph.append(Q)
                self.w0_graph.append(w)
        self.Dn_list = []
        with open(FILE_NAME_DATA_DN, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')  # <csv.DictReader object at 0x03B11030>
            for row in reader:
                Dn = row['Dn']
                self.Dn_list.append(Dn)
        self.list_with_main_pumps = []
        with open(FILE_DATA_MAIN_PUMPS, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')  # <csv.DictReader object at 0x03B11030>
            for row in reader:
                brand = row['Brand']
                rotor = row['Rotor']
                impeller_diameter = row['Impeller diameter']
                a = float(check_comma(row['a']))
                b = float(check_comma(row['b']))
                Q_nom = float(check_comma(row['Qnom']))
                kaf = float(check_comma(row['k']))
                self.list_with_main_pumps.append([brand, rotor, impeller_diameter, a, b, Q_nom, kaf])
        self.list_with_main_pumps.sort(key=lambda k: k[5])
        self.list_with_suport_pumps = []
        with open(FILE_DATA_SUPPORT_PUMPS, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')  # <csv.DictReader object at 0x03B11030>
            for row in reader:
                brand = row['Brand']
                impeller_diameter = row['Impeller diameter']
                a = float(check_comma(row['a']))
                b = float(check_comma(row['b']))
                Q_nom = float(check_comma(row['Qnom']))
                self.list_with_suport_pumps.append([brand, impeller_diameter, a, b, Q_nom])
        self.list_with_suport_pumps.sort(key=lambda k: k[4])
        list_names = []
        list_causes = []
        list_values = []
        with open(FILE_DATA_COEFFICIENTS, 'r') as csvfile:
            reader = csv.DictReader(csvfile, delimiter=';')  # <csv.DictReader object at 0x03B11030>
            for row in reader:
                name = row['Name']
                cause = row['Сause']
                value = float(check_comma(row['Value']))
                list_names.append(name)
                list_causes.append(cause)
                list_values.append(value)
        self.database = peewee.SqliteDatabase('source_data.db')
        self.dict_data_infor_kaf = {}
        for index, kaf in enumerate(list_names):
            if kaf != kaf or list_causes[index] != list_causes[index] or \
                    list_values[index] != list_values[index]:
                continue
            if kaf not in self.dict_data_infor_kaf.keys():
                self.dict_data_infor_kaf[kaf] = [
                    [list_causes[index], list_values[index]]]
            else:
                self.dict_data_infor_kaf[kaf].append(
                    [list_causes[index], list_values[index]])

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
    creator_data_base = CreatorDataBase(NAME_DATA_BASE)
    creator_data_base.run()
