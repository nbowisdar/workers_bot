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

# """СЕРПЕНЬ - Ляхов Ілля Михайлович
# 94,5 денних годин х 90,13= 8517,29грн
# 49,5 нічних годин × 102,64 = 5080,68грн
# В сумі 13597,97, з яких 70% до оплати - 9518,58грн та 30% КПІ - 4079,39грн"""
"""30% КПІ 
- 5%+5% швидкість чатів та мейлів - 90% і 100% відповідно (1291,81 грн)
- 20% крі - 80% (2175,67грн)
в сумі за КПІ - 3467,48грн"""


def build_kpi_msg(kpi: dict, kpi_pos: dict) -> str:
    msg = ""
    for k, v in kpi.items():
        msg += f"\t\t\t\t {k} - <b>{kpi_pos[k]}</b>% (Виконано на - <b>{v}</b>%)\n"
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
          f"70% до оплати - <b>{round(calc_data['earned']/100*70, 2)}</b> грн." \
          f" та 30% КПІ - <b>{round(calc_data['earned']/100*30, 2)}</b> грн.\n" \
          f"КПІ: \n" + build_kpi_msg(kpi, info['kpi'])

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
