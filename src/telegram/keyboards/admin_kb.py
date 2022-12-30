from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb1 = [
    [KeyboardButton(text="Показати всіх"), KeyboardButton(text="Детальніше про працівника")],
    [KeyboardButton(text="Додати нову зміну"), KeyboardButton(text="Видалити працівника")],
    [KeyboardButton(text="Додати нового працівника"),KeyboardButton(text="Оновити інфармацію про працівника")],

]

admin_kb_main = ReplyKeyboardMarkup(
    keyboard=kb1,
    resize_keyboard=True
)

kb2 = [
    [KeyboardButton(text="Так"), KeyboardButton(text="Ні")]
]

yes_or_no_kb = ReplyKeyboardMarkup(
    keyboard=kb2,
    resize_keyboard=True
)


next_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="Далі (залишити як є)")]],
    resize_keyboard=True
)
