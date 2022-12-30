from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


_kb1 = [
    [KeyboardButton(text='Я працівник👷‍♂️'), KeyboardButton(text='admin🧑‍💻')]
]

start_kb = ReplyKeyboardMarkup(
    keyboard=_kb1,
    resize_keyboard=True
)


_kb2 = [
    [KeyboardButton(text="Відмінити")]
]

cancel_kb = ReplyKeyboardMarkup(
    keyboard=_kb2,
    resize_keyboard=True
)


_kb3 = [
    [KeyboardButton(text="Обрати дату:"), KeyboardButton(text="Обрати період:")],
    [KeyboardButton(text="Назад")]
]

choose_time_btn = ReplyKeyboardMarkup(
    keyboard=_kb3,
    resize_keyboard=True
)


_kb4 = [
    [KeyboardButton(text="Структура компанії") ]

]

choose_information_btn = ReplyKeyboardMarkup(
    keyboard=_kb4,
    resize_keyboard=True
)

# _kb3 = [
#     [KeyboardButton(text="По сьогодні")]
# ]

until_kb = ReplyKeyboardMarkup(
    keyboard=_kb2,
    resize_keyboard=True
)

today_btn = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Сьогоднішня дата")]],
    resize_keyboard=True
)
