from src.database.tables import db, Worker, WorkShift
from src.schema import UserModel, ShiftModel, TimePerModel, YearMonth
from src.my_logger import logger


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
            date=shift.date
        ))
    return shifts_data


def _get_user_model(user: Worker) -> UserModel:
    return UserModel(
        worker_id=user.worker_id,
        name=user.name,
        surname=user.surname,
        phone=user.phone,
        email=user.email,
        tag=user.tag,
        department=user.department,
        position=user.position,
        status=user.status,
        kpi=user.kpi,
        skill=user.skill,
        wage_day=user.wage_day,
        wage_night=user.wage_night,
        note=user.note,
        employment_date=user.employment_date,
        shifts=_workers_shift(user)

    )


def get_all_workers() -> list[UserModel]:
    return [_get_user_model(user) for user in Worker.select()]


def get_all_workers_id() -> list[int]:
    return [_get_user_model(user)['worker_id'] for user in Worker.select()]


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
    user.kpi = user_new_data['kpi']
    user.skill = user_new_data['skill']
    user.wage_day = user_new_data['wage_day']
    user.wage_night = user_new_data['wage_night']
    user.employment_date = user_new_data['employment_date']
    user.save()
    logger.info(f'User updated {user.worker_id}')


def get_one_shift(worker_id: int, date: str) -> ShiftModel | None:
    worker = Worker.get_or_none(worker_id=worker_id)
    if not worker:
        raise Exception("User doesnt exist")
    # TODO maybe doesn't work
    shift = worker.shifts.where(WorkShift.date == date).get_or_none()
    if not shift:
        return
    return ShiftModel(
        worker_id=shift.worker_id,
        day_hours=shift.day_hours,
        night_hours=shift.night_hours,
        date=shift.date,
        earned=(shift.day_hours*worker.wage_day+shift.night_hours*worker.wage_night)*70/100+(shift.day_hours*worker.wage_day+shift.night_hours*worker.wage_night)*worker.kpi/100*30/100+(shift.day_hours*worker.wage_day+shift.night_hours*worker.wage_night)*5/100*worker.skill,
        #qwe=100
    )


def get_shifts(data: TimePerModel) -> list[ShiftModel]:
    worker = Worker.get_or_none(worker_id=data.worker_id)
    result = []
    if not worker:
        raise Exception("User doesnt exist")
    # TODO maybe doesn't work
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
            earned=(shift.day_hours*worker.wage_day+shift.night_hours*worker.wage_night)*70/100+(shift.day_hours*worker.wage_day+shift.night_hours*worker.wage_night)*worker.kpi/100*30/100,
            #qwe=100
        ))
    return result


def get_wage_data_by_month(data: YearMonth):
    worker = Worker.get_or_none(worker_id=data.worker_id)
    if not worker:
        raise Exception("User doesnt exist")
    result = []
    cur_date = f"{data.year}/{data.month}"
    print(cur_date)
    # TODO end this function


if __name__ == '__main__':
    user = Worker.get(worker_id=286365412)#.where(Worker.worker_id == 123)
    x = user.shifts.where(WorkShift.date > "20/12/2023").get_or_none()
    print(x)
    #print(x.day_hours)
