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

#datetime_object = datetime.strptime(x, '%y/%m/%d').date()

