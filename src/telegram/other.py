import json
from datetime import date, datetime


def check_date_format(date: str):
    year, month, day = map(int, date.split('/'))
    if month > 12 or month < 0:
        raise Exception('Wrong month')
    elif day > 31 or day < 0:
        raise Exception('Wrong month')
    elif year < 2000 or year > 2050:
        raise Exception('Wrong year')


months = ["січень", "лютий", "березень", "квітень", "травень",
          "червень", "липень", "серпень", "вересень",
          "жовтень", "листопад", "грудень"]


def get_num_month(month: str) -> int:
    return months.index(month) + 1


def extract_kpi_data(text_json: str) -> str:
    rez = ""
    for key, value in json.loads(text_json).items():
        rez += f"{key} - *{value}*% \n"
    return rez


