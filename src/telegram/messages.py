from pprint import pprint
import json
from src.schema import UserModel, ShiftModel, PositionModel, ShiftsData
from src.database import get_all_workers
from src.telegram.other import extract_kpi_data


def generate_message_with_user_info(user: UserModel) -> str:
    msg = f"""
            {user['name']}  {user['surname']}
            id - {user['worker_id']}
            Телефон - {user['phone']}
            Пошта - {user['email']}
            Відділ - {user['department']}
            Посада - {user['position']['name']}
            Статус - {user['status']} 
            Дата працевлаштування - {user['employment_date']}
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


# def message_about_plural_shifts(shifts: ShiftsData) -> str:
#     msg = f"""
#             З *{shifts['date_from']}* по *{shifts['date_to']}* : \n
#             Всього у день відпрацевано - *{shifts['days_hours']} год.* \n
#             Всього у ніч відпрацевано - *{shifts['nights_hours']} год.* \n
#             За цей проміжок часу ви заробили *{shifts['earned']} грн.*
#             """
#     return msg


def message_with_all_users(users: list[UserModel]) -> str:
    msg = ''
    for user in users:
        msg += f"{user['name']} {user['surname']}, id - `{user['worker_id']}` \n"

    if not msg:
        return "У вас ще немає працівників"
    return "Усі працівники:\n" + msg


def build_kpi_msg(kpi: dict, kpi_pos: dict, calc_data: dict) -> str:
    msg = ""
    for k, v in kpi.items():
        full_earned = calc_data['all_days_earned'] + calc_data['all_night_earned']
        e = round((full_earned / 100 * kpi_pos[k])/100*v, 2)
        msg += f"\t\t\t\t {k} - <b>{kpi_pos[k]}</b>% (Виконано на - <b>{v}</b>%)\n - {e} грн. \n"
    return msg


def build_month_wage_message(info: ShiftsData) -> str:
    calc_data = info['calculated_data']
    kpi = calc_data['kpi_data_calculated']
    wage_d = info['wage_day'] + info['wage_day']/100*info['skill']
    wage_n = info['wage_night'] + info['wage_night']/100*info['skill']
    msg = f"{info['date'].capitalize()} - {info['full_name']} \n" \
          f"{calc_data['all_days_hours']} ч. день * <b>{wage_d}</b> грн. = {calc_data['all_days_earned']} грн.\n" \
          f"{calc_data['all_days_hours']} ч. ніч * <b>{wage_n}</b> грн. = {calc_data['all_night_earned']} грн.\n" \
          f"В сумі <b>{calc_data['earned']} грн.</b> з яких:\n" \
          f"70% до оплати - <b>{calc_data['earned_stable']}</b> грн." \
          f" та 30% КПІ - <b>{calc_data['earned_kpi']}</b> грн.\n"  \
          f"КПІ: \n" + build_kpi_msg(kpi, info['kpi'], calc_data)

    return msg


def msg_with_positions(positions: list[PositionModel]) -> str:
    msg = ""
    for pos in positions:
        kpi_part = extract_kpi_data(pos['kpi_data'])
        msg += f"""Позиція: *{pos['name']}*

Оплата день: *{pos['wage_day']}* грн.
Оплата ніч: *{pos['wage_night']}* грн.
Сумма KPI: *{pos['kpi']}*
{kpi_part}"""
        msg += "----------------------------------------\n"
    return msg


text_json = str
def get_kpi_template(text: text_json) -> str:
    msg = ""
    data = json.loads(text)
    for key in data.keys():
        msg += f"{key}->100 "
    return '`' + msg + '`'
