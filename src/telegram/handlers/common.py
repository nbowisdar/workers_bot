from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Text
from aiogram3_calendar import SimpleCalendar
from src.schema import WorkerAndBtn
from src.telegram.handlers.fsm_handlers import TimePer, OneDay
from src.telegram.keyboards import start_kb, choose_time_btn, user_main_kb, admin_kb_main, today_btn, user_emp_date, \
    user_information, cancel_kb
from src.database import get_user, get_one_shift, get_shifts
from src.telegram.messages import generate_message_with_user_info, message_about_one_shift, generate_message_with_emp_date, generate_message_with_information
from src.telegram.handlers.admin import admins
from aiogram.fsm.context import FSMContext
from src.telegram.setup import common_router


def is_admin(telegram_id: int) -> bool:
    if telegram_id in admins:
        return True
    return False


@common_router.message(Text(text="Назад"))
@common_router.message(Command(commands='start'))
async def start(message: Message):
    await message.answer("Головна сторінка", reply_markup=start_kb)


@common_router.message(Text(text="Робоча статистика"))
async def choose_time(message: Message):
    await message.answer("Бажаєте подивитися за конкретну дату, \n"
                         "або за проміжок часу?",
                         reply_markup=choose_time_btn)


@common_router.message(Text(text="Обрати дату:"))
async def one_day_stat(message: Message, state: FSMContext):
    if is_admin(message.from_user.id):
        await state.set_state(OneDay.worker_id)
        await message.answer("Введіть id працівника:", reply_markup=cancel_kb)
        await state.update_data(is_admin=True)
        await state.update_data(reply_btn=admin_kb_main)

    else:
        await state.update_data(is_admin=False)
        await state.update_data(worker_id=message.from_user.id)
        await state.update_data(reply_btn=user_main_kb)
        await state.set_state(OneDay.date)
        await message.reply("Введіть дату у наступному форматі: \n"
                            "*Рік/Місяць/День* \n"
                            "Приклад: 2015/10/20",
                            reply_markup=today_btn,
                            parse_mode="MARKDOWN")


@common_router.message(Text(text="Обрати період:"))
async def period_stat(message: Message, state: FSMContext):
    if is_admin(message.from_user.id):
        await state.set_state(TimePer.worker_id)
        await message.answer("Введіть id працівника:", reply_markup=cancel_kb)
        await state.update_data(is_admin=True)
        await state.update_data(reply_btn=admin_kb_main)

    else:
        await state.update_data(is_admin=False)
        await state.update_data(worker_id=message.from_user.id)
        await state.update_data(reply_btn=user_main_kb)
        await state.set_state(TimePer.time_start)
        await message.answer("Оберіть число з якого бажаете статистику \n"
                             "Приклад: `2015/10/20`",
                             reply_markup=ReplyKeyboardRemove(),
                             parse_mode="MARKDOWN")