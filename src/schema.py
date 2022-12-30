from typing import TypedDict, NamedTuple
from aiogram.types import ReplyKeyboardMarkup


class WithWage(TypedDict):
    earned: float
    worker_id: int


class ShiftModel(WithWage):
    day_hours: float
    night_hours: float
    date: str


class manager_kpi(WithWage):
    user_kpi: list[ShiftModel] | None


class PluralShifts(WithWage):
    days_hours: float
    nights_hours: float
    date_from: str
    date_to: str


class UserModel(TypedDict):
    worker_id: int
    name: str
    surname: str
    phone: str
    email: str
    tag: str
    department: str
    position: str
    status: str
    kpi: float
    skill: float
    employment_date: str
    wage_day: float
    wage_night: float
    note: str
    shifts: list[ShiftModel] | None


class TimePerModel(NamedTuple):
    is_admin: bool
    worker_id: int
    reply_btn: ReplyKeyboardMarkup
    time_start: str
    time_finish: str


class WorkerAndBtn(NamedTuple):
    worker_id: int
    btn: ReplyKeyboardMarkup
    is_admin: bool


class YearMonth(NamedTuple):
    worker_id: int
    year: str
    month: str
