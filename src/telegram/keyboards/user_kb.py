from aiogram.types import KeyboardButton, ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from src.telegram.other import months

_kb1 = [
    [KeyboardButton(text="Мій профіль"), KeyboardButton(text="Робоча статистика")],
    [KeyboardButton(text="Заробітня плата"), KeyboardButton(text="Загальна інформація")],
    [KeyboardButton(text="Назад")]
]

user_main_kb = ReplyKeyboardMarkup(
    keyboard=_kb1,
    resize_keyboard=True
)
user_emp_date = ReplyKeyboardMarkup(
    keyboard=_kb1,
    resize_keyboard=True
)
user_information = ReplyKeyboardMarkup(
    keyboard=_kb1,
    resize_keyboard=True
)


def get_years_kb():
    builder = ReplyKeyboardBuilder()
    for year in range(2017, 2024):
        builder.add(KeyboardButton(text=str(year)))
    builder.adjust(3)
    return builder.as_markup(resize_keyboard=True)


def get_months_kb():
    builder = ReplyKeyboardBuilder()
    for month in months:
        builder.add(KeyboardButton(text=str(month)))
    builder.adjust(4)
    return builder.as_markup(resize_keyboard=True)
