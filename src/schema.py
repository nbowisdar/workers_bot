from datetime import datetime
from typing import TypedDict, NamedTuple
from aiogram.types import ReplyKeyboardMarkup


class WithWage(TypedDict):
    worker_id: int
    full_name: str
    skill: float
    kpi: dict


class ShiftModel(WithWage):
    kpi_data: str
    day_hours: float
    night_hours: float
    # kpi_data: str
    date: str
    earned: float


class Shifts(WithWage):
    shifts: list[ShiftModel]
    earned: float
    kpi_data_calculated: str
    date: str


class CalcModel(TypedDict):
    all_days_hours: float
    all_night_hours: float
    all_days_earned: float
    all_night_earned: float
    earned: float
    earned_stable: float
    earned_kpi: float
    kpi_data_calculated: dict


class ShiftsData(WithWage):
    date: str
    calculated_data: CalcModel
    wage_day: float
    wage_night: float
    # kpi_data_calculated: str



text_json = str
class PositionModel(TypedDict):
    name: str
    kpi: float
    kpi_data: text_json
    wage_day: float
    wage_night: float
    #workers: list[UserModel] | None


class UserModel(TypedDict):
    worker_id: int
    name: str
    surname: str
    phone: str
    email: str
    tag: str
    department: str
    position: PositionModel
    status: str
    employment_date: str
    skill: float
    note: str
    shifts: list[ShiftModel] | None


class TimePerModel(NamedTuple):
    is_admin: bool
    worker_id: int
    reply_btn: ReplyKeyboardMarkup
    time_start: datetime
    time_finish: datetime


class WorkerAndBtn(NamedTuple):
    worker_id: int
    btn: ReplyKeyboardMarkup
    is_admin: bool


class YearMonth(NamedTuple):
    worker_id: int
    year: str
    month: str


class TwoDates(NamedTuple):
    worker_id: int
    start_date: datetime
    up_to_date: datetime

