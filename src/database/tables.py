from peewee import SqliteDatabase, Model, CharField, FloatField, \
    TextField, IntegerField, ForeignKeyField, DateField
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent
db = SqliteDatabase(BASE_DIR / 'data.db')

# база даних пыдключаэться тут


class BaseModel(Model):
    class Meta:
        database = db


class Position(BaseModel):
    name = CharField(unique=True)
    kpi = FloatField(null=True)
    kpi_data = CharField()
    wage_day = FloatField()
    wage_night = FloatField()


class Worker(BaseModel):
    worker_id = IntegerField(primary_key=True)
    name = CharField()
    surname = CharField()
    phone = CharField()
    email = CharField()
    tag = TextField()
    department = CharField()
    status = CharField()
    note = TextField()
    employment_date = DateField()
    skill = FloatField(default=0)
    position = ForeignKeyField(Position, backref="workers")


class WorkShift(BaseModel):
    worker = ForeignKeyField(Worker, backref='shifts', on_delete='CASCADE')
    day_hours = FloatField()
    night_hours = FloatField()
    kpi_data = CharField()
    date = DateField()


def create_db():
    db.create_tables([Worker, WorkShift, Position])


if __name__ == '__main__':
    x = Worker.get(worker_id=286365412)
    print(x.employment_date)
    print(x.skill)


