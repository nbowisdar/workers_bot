from src.schema import UserModel, ShiftModel, PluralShifts
from src.database import get_all_workers


def generate_message_with_user_info(user: UserModel) -> str:
    msg = f"""
{user['name']}  {user['surname']}      
id - {user['worker_id']} \n
{user['tag']}
{user['phone']}
{user['email']} \n
Відділ - {user['department']}
Посада - {user['position']}
Статус - {user['status']} 
Дата працевлаштування - {user['employment_date']} \n
Нотатка - {user['note']}
            """
    return msg


def generate_message_with_emp_date(user: UserModel) -> str:
    msg = f"""
123
            """
    return msg



def generate_message_with_information(user: UserModel) -> str:
    msg = f"""
    тут буде про information
    
id- {user['worker_id']} \n

            """
    return msg


def generate_message_general_information(user: UserModel) -> str:
    msg = f"""
    тут буде про general_information

id- {user['worker_id']} \n

            """
    return msg


def message_about_one_shift(shift: ShiftModel) -> str:
    msg = f"""
            Інформація про робочу зміну: \n
            Годин у день - *{shift['day_hours']} \n
            Годин у ніч - *{shift['night_hours']} \n
            Дата - *{shift['date']} \n
            цццуу *{shift.qwe}  \n
            За цю добу ви заробили(з без КПІ та досвідом        ) - *{shift.earned}
            """
    return msg


def message_about_plural_shifts(shifts: PluralShifts) -> str:
    msg = f"""
            З *{shifts['date_from']}* по *{shifts['date_to']}* : \n
            Всього у день відпрацевано - *{shifts['days_hours']} год.* \n
            Всього у ніч відпрацевано - *{shifts['nights_hours']} год.* \n
            За цей проміжок часу ви заробили *{shifts['earned']} грн.*
            """
    return msg


def message_with_all_users(users: list[UserModel]) -> str:
    msg = ''
    for user in users:
        msg += f"{user['name']} {user['surname']}, id - `{user['worker_id']}` \n"

    if not msg:
        return "У вас ще немає працівників"
    return "Усі працівники:\n" + msg


def build_month_wage_message(wage_info) -> str:
    msg = "ok"
    ...
    return msg
