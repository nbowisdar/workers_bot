import json

from dateutil.relativedelta import relativedelta

from src.database.tables import db, Worker, WorkShift, Position
from src.schema import UserModel, ShiftModel, TimePerModel, YearMonth, PositionModel, Shifts, ShiftsData, CalcModel
from src.my_logger import logger
from datetime import datetime


def create_worker(user: UserModel):
    Worker.create(**user)


def create_shift(data: ShiftModel):
    WorkShift.create(**data)


def _workers_shift(user: Worker) -> list[ShiftModel]:
    shifts = user.shifts
    shifts_data = []
    for shift in shifts:
        shifts_data.append(ShiftModel(
            worker_id=shift.worker,
            day_hours=shift.day_hours,
            night_hours=shift.night_hours,
            kpi_data=shift.kpi_data,
            date=shift.date
        ))
    return shifts_data


def _get_user_position(user: Worker) -> PositionModel:
    return PositionModel(
        name=user.position.name,
        kpi=user.position.kpi,
        wage_day=user.position.wage_day,
        wage_night=user.position.wage_night,
    )


def _get_user_model(user: Worker) -> UserModel:
    return UserModel(
        worker_id=user.worker_id,
        name=user.name,
        surname=user.surname,
        phone=user.phone,
        email=user.email,
        tag=user.tag,
        department=user.department,
        position=_get_user_position(user),
        status=user.status,
        # kpi=user.kpi,
        skill=user.skill,
        # wage_day=user.wage_day,
        # wage_night=user.wage_night,
        note=user.note,
        employment_date=user.employment_date,
        shifts=_workers_shift(user)

    )


def get_all_workers() -> list[UserModel]:
    return [_get_user_model(user) for user in Worker.select()]


def get_all_workers_id() -> list[int]:
    return [_get_user_model(user)['worker_id'] for user in Worker.select()]


def create_position(pos: PositionModel):
    Position.create(**pos).save()
    logger.info(f"created new position - {pos['name']}")


def _get_pos_model(pos: Position) -> PositionModel:
    return PositionModel(
        name=pos.name,
        kpi=pos.kpi,
        kpi_data=pos.kpi_data,
        wage_day=pos.wage_day,
        wage_night=pos.wage_night
    )


def get_all_position() -> list[PositionModel]:
    return [_get_pos_model(pos) for pos in Position.select()]


def get_pos_by_name(pos_name: str, get_model=False) -> PositionModel | Position:
    pos = Position.get(name=pos_name)
    if get_model:
        return _get_pos_model(pos)
    return pos


def get_user(worker_id: int) -> UserModel:
    user = Worker.get_or_none(worker_id=worker_id)
    return _get_user_model(user)


def drop_user(worker_id: int):
    Worker.delete().where(Worker.worker_id == worker_id).execute()


def update_user(user_new_data: UserModel):
    user = Worker.get(worker_id=user_new_data['worker_id'])
    user.worker_id = user_new_data['worker_id']
    user.name = user_new_data['name']
    user.surname = user_new_data['surname']
    user.phone = user_new_data['phone']
    user.email = user_new_data['email']
    user.tag = user_new_data['tag']
    user.department = user_new_data['department']
    user.position = user_new_data['position']
    user.status = user_new_data['status']
    # user.kpi = user_new_data['kpi']
    user.skill = user_new_data['skill']
    # user.wage_day = user_new_data['wage_day']
    # user.wage_night = user_new_data['wage_night']
    user.employment_date = user_new_data['employment_date']
    user.save()
    logger.info(f'User updated {user.worker_id}')


def get_one_shift(worker_id: int, date: str) -> ShiftModel | None:
    worker = Worker.get_or_none(worker_id=worker_id)
    if not worker:
        raise Exception("User doesnt exist")
    shift = worker.shifts.where(WorkShift.date == date).get_or_none()
    if not shift:
        return
    return ShiftModel(
        worker_id=shift.worker_id,
        day_hours=shift.day_hours,
        night_hours=shift.night_hours,
        date=shift.date,

        earned=(shift.day_hours * worker.wage_day + shift.night_hours * worker.wage_night) * 70 / 100 + (
                shift.day_hours * worker.wage_day + shift.night_hours * worker.wage_night) * worker.kpi / 100 * 30 / 100 + (
                shift.day_hours * worker.wage_day + shift.night_hours * worker.wage_night) * 5 / 100 * worker.skill,
        # qwe=100
    )


def get_shifts(data: TimePerModel) -> list[ShiftModel]:
    worker = Worker.get_or_none(worker_id=data.worker_id)
    result = []
    if not worker:
        raise Exception("User doesnt exist")
    shifts = worker.shifts.select().where(
        data.time_start <= WorkShift.date
    ).where(
        (WorkShift.date >= data.time_start) &
        (data.time_finish >= WorkShift.date)
    )
    for shift in shifts:
        result.append(ShiftModel(
            worker_id=shift.worker_id,
            day_hours=shift.day_hours,
            night_hours=shift.night_hours,
            date=shift.date,
            earned=(shift.day_hours * worker.wage_day + shift.night_hours * worker.wage_night) * 70 / 100 + (
                    shift.day_hours * worker.wage_day + shift.night_hours * worker.wage_night) * worker.kpi / 100 * 30 / 100,
            # qwe=100
        ))
    return result


# def _calculate_hours(shifts: list[WorkShift]) -> tuple[int, int]:
#     all_day = 0
#     all_night = 0
#     for shift in shifts:
#         all_day += shift.day_hours
#         all_night += shift.night_hours
#
#     return all_day, all_night


def _calc_kpi_part(s: int, shift: WorkShift, pos: Position) -> float:
    pos_kpi = list(json.loads(pos.kpi_data).values())
    shift_kpi = list(json.loads(shift.kpi_data).values())
    result = 0
    s = s / 100 * pos.kpi
    for i in range(len(pos_kpi)):
        result += (s / 100 * pos_kpi[i]) / 100 * shift_kpi[i]
    return round(result, 2)


def _update_kpi(kpi_data: dict, shifts: list[WorkShift]) -> dict:
    kpi_keys = list(kpi_data.keys())
    result = {}
    count_shift = 0
    for shift in shifts:
        kpi_cur = json.loads(shift.kpi_data)
        for key in kpi_keys:
            prev = result.get(key, 0)
            result[key] = prev + kpi_cur[key]

        count_shift += 1
    for k, v in result.items():
        result[k] = round(v/count_shift, 2)
    return result


def _calculate_shifts_data(*, shifts: list[WorkShift], worker: Worker) -> CalcModel:
    earned = 0
    all_days_h = 0
    all_earned_day = 0
    all_night_h = 0
    all_earned_night = 0
    skill = worker.skill
    wg_d = worker.position.wage_day
    wg_n = worker.position.wage_night
    kpi_data_calculated = _update_kpi(json.loads(worker.position.kpi_data), shifts)
    for shift in shifts:
        earned_day = shift.day_hours * (wg_d+(wg_d/100*skill))
        earned_night = shift.night_hours * (wg_n+(wg_n/100*skill))
        s = earned_day + earned_night
        earned += (s * 70 / 100) + _calc_kpi_part(s, shift, worker.position)  # (s * 30 / 100 * kpi) # / 100
        all_days_h += shift.day_hours
        all_night_h += shift.night_hours
        all_earned_day += earned_day
        all_earned_night += earned_night
    print(earned)
    return CalcModel(
        all_days_hours=all_days_h,
        all_night_hours=all_night_h,
        all_days_earned=all_earned_day,
        all_night_earned=all_earned_night,
        earned=round(earned, 2),
        kpi_data_calculated=kpi_data_calculated
    )


def get_wage_data_by_month(data: YearMonth, month: str) -> ShiftsData:
    worker = Worker.get_or_none(worker_id=data.worker_id)
    if not worker:
        raise Exception("User doesnt exist")
    start_date = datetime.strptime(f"{data.year}/{data.month}/01", "%Y/%m/%d")
    up_to_date = start_date + relativedelta(day=31)

    shifts = worker.shifts.where((WorkShift.date >= start_date) &
                                 (WorkShift.date <= up_to_date))
    return ShiftsData(
        worker_id=worker.worker_id,
        full_name=f"{worker.name} {worker.surname}",
        skill=worker.skill,
        wage_day=worker.position.wage_day,
        wage_night=worker.position.wage_night,
        date=month,
        kpi=json.loads(worker.position.kpi_data),
        calculated_data=_calculate_shifts_data(worker=worker, shifts=shifts)
        )


def get_workers_kpi(worker_id: int) -> str:
    worker = Worker.get(worker_id=worker_id)
    return worker.position.kpi_data





if __name__ == '__main__':
    user = Worker.get(worker_id=286365412)  # .where(Worker.worker_id == 123)
    d = datetime.strptime("20/12/2023", "%d/%m/%Y")
    x = user.shifts.where(WorkShift.date > d)
    print(x)
    # print(x.day_hours)
    # pos = get_pos_by_name('dev')
    # print(pos)
