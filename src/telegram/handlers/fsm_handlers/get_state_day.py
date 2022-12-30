from aiogram.types import CallbackQuery
from aiogram3_calendar import SimpleCalendar, simple_cal_callback
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from datetime import datetime, date
from src.my_logger import logger
from aiogram.types import Message
from src.database import get_all_workers_id
from src.database import get_one_shift, create_shift
from src.schema import WorkerAndBtn
from src.telegram.messages import message_about_one_shift
from src.telegram.setup import common_router, admins
from src.telegram.keyboards import admin_kb_main, today_btn


class OneDay(StatesGroup):
    is_admin = State()
    worker_id = State()
    reply_btn = State()
    wage_day = State()
    wage_night = State()
    date = State()



@common_router.message(OneDay.worker_id)
async def is_admin_or_user(message: Message, state: FSMContext):
    try:
        worker_id = int(message.text)
        await state.update_data(worker_id=worker_id)
        await state.set_state(OneDay.date)
        await message.reply("Вкажіть дату: \n"
                            "Введіть дату у наступному форматі: \n"
                            "*Рік/Місяць/День* \n"
                            "Приклад: `2015/10/20`",
                            reply_markup=today_btn,
                            parse_mode="MARKDOWN")
    except ValueError:
        await message.reply("Повинно бути число!",
                            reply_markup=admin_kb_main)
        await state.clear()


@common_router.message(OneDay.date)
async def from_time(message: Message, state: FSMContext):
    try:
        if message.text.lower() == "сьогоднішня дата":
            cur_date = date.today()
        else:
            cur_date = datetime.strptime(message.text, "%Y/%m/%d").date()
        print(cur_date)
        await state.update_data(date=cur_date)
        data = await state.get_data()

        await show_rez(message, data)

    except Exception as err:
        logger.error(err)
        data = await state.get_data()
        await message.reply("Не вірний формат!",
                            reply_markup=data["reply_btn"])
    finally:
        await state.clear()


async def show_rez(message: Message, data: dict):
    shift_info = get_one_shift(data["worker_id"], data["date"])
    if not shift_info:
        await message.answer("Нема данних про цю дату.",
                             reply_markup=data["reply_btn"])
    else:
        msg = message_about_one_shift(shift_info)
        await message.answer(msg,
                             reply_markup=data["reply_btn"],
                             parse_mode="MARKDOWN")
