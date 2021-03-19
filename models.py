import peewee
from playhouse.sqlite_ext import SqliteExtDatabase

database = SqliteExtDatabase('source_data.db', regexp_function=True, timeout=3,
                             pragmas={'journal_mode': 'wal'})


class BaseTable(peewee.Model):
    # В подклассе Meta указываем подключение к той или иной базе данных
    class Meta:
        database = database


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


class PipeTable(BaseTable):
    brand = peewee.CharField()
    diameter = peewee.FloatField()
    R1n = peewee.FloatField()
    k1 = peewee.FloatField()


class CoordinatesTable(BaseTable):
    var = peewee.CharField()
    json_coordinates = peewee.CharField()


class SourceDataTable(BaseTable):
    var = peewee.CharField()
    json_data = peewee.CharField()


class ActionVarTable(BaseTable):
    var = peewee.CharField()
    name_action = peewee.CharField()


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
