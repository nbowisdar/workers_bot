from datetime import datetime, date
from pprint import pprint

from src.my_logger import logger
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from src.database import get_shifts, ShiftModel
from src.schema import PluralShifts, TimePerModel
from src.telegram.keyboards import until_kb, user_main_kb, today_btn, admin_kb_main
from src.telegram.messages import message_about_plural_shifts
from src.telegram.setup import common_router
from aiogram3_calendar import SimpleCalendar, simple_cal_callback


def calculate_stat(shifts: list[ShiftModel]) -> PluralShifts:
    all_days_hours = 0
    all_nights_hours = 0
    earned = 0
    qwe = 0
    for shift in shifts:
        all_days_hours += shift['day_hours']
        all_nights_hours += shift['night_hours']
        earned += shift['earned']
        qwe += shift['qwe']

    return PluralShifts(
        days_hours=all_days_hours,
        nights_hours=all_nights_hours,
        earned=earned,
        qwe=qwe,
        date_from=shifts[0]['date'],
        date_to=shifts[-1]['date']
    )


class TimePer(StatesGroup):
    is_admin = State()
    worker_id = State()
    reply_btn = State()
    time_start = State()
    time_finish = State()


@common_router.message(TimePer.worker_id)
async def is_admin_or_user(message: Message, state: FSMContext):
    try:
        worker_id = int(message.text)
        await state.update_data(worker_id=worker_id)
        await state.set_state(TimePer.time_start)
        await message.reply("Вкажіть початкову дату:date = State()\n"
                            "Введіть дату у наступному форматі: \n"
                            "*Рік/Місяць/День* \n"
                            "Приклад: `2015/10/20`",
                            reply_markup=ReplyKeyboardRemove(),
                            parse_mode="MARKDOWN")
    except ValueError:
        await message.reply("Повинно бути число!",
                            reply_markup=admin_kb_main)
        await state.clear()


@common_router.message(TimePer.time_start)
async def from_time(message: Message, state: FSMContext):
    try:
        cur_date = datetime.strptime(message.text, "%Y/%m/%d").date()
        await state.update_data(time_start=cur_date)
        await state.set_state(TimePer.time_finish)
        await message.reply("По яку дату потрібна інформація?",
                            reply_markup=today_btn)
    except Exception as err:
        logger.error(err)
        data = await state.get_data()
        await state.clear()
        await message.reply("Не вірний формат!",
                            reply_markup=data["reply_btn"])


@common_router.message(TimePer.time_finish)
async def set_until_time(message: Message, state: FSMContext):
    data = await state.get_data()
    try:
        if message.text.lower() == "сьогоднішня дата":
            cur_date = date.today()
        else:
            cur_date = datetime.strptime(message.text, "%Y/%m/%d").date()
        await state.update_data(time_finish=cur_date)
        data = await state.get_data()
        await show_results(message, data)
    except Exception as err:
        logger.error(err)
        await message.reply("Не вірний формат!",
                            reply_markup=data["reply_btn"])
    finally:
        await state.clear()


async def show_results(message: Message, data: dict):
    struct_data = TimePerModel(**data)
    all_shifts = get_shifts(struct_data)
    if not all_shifts:
        await message.answer("Немає данних про вас", reply_markup=data['reply_btn'])
        return
    info = calculate_stat(all_shifts)
    msg = message_about_plural_shifts(info)
    await message.answer(msg,
                         reply_markup=data['reply_btn'],
                         parse_mode="MARKDOWN")
