from pprint import pprint
from src.database import create_shift
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from src.telegram.setup import admin_router
from aiogram3_calendar import SimpleCalendar, simple_cal_callback
from src.telegram.keyboards import admin_kb_main, today_btn
from src.my_logger import logger
from src.database import get_all_workers_id
from datetime import datetime, date

class Shift(StatesGroup):
    worker_id = State()
    day_hours = State()
    night_hours = State()
    date = State()



@admin_router.message(Shift.worker_id)
async def set_worker_id(message: Message, state: FSMContext):
    all_workers_id = get_all_workers_id()
    try:
        if int(message.text) not in all_workers_id:
            raise Exception('not allowed')
        await state.update_data(worker_id=int(message.text))
        await state.set_state(Shift.day_hours)
        await message.reply("Кількість відпрацьованих годин в день:🌕")
    except Exception as err:
        logger.error(err)
        await state.clear()
        await message.reply("Працівник з таким id не існує!🛑",
                            reply_markup=admin_kb_main)


@admin_router.message(Shift.day_hours)
async def set_day(message: Message, state: FSMContext):
    try:
        await state.update_data(day_hours=float(message.text))
        await state.set_state(Shift.night_hours)
        await message.reply("Кількість відпрацьованих годин в ніч:🌚")
    except ValueError:
        await state.clear()
        await message.reply('Помилка! Введіть число🛑',
                            reply_markup=admin_kb_main)


@admin_router.message(Shift.night_hours)
async def set_night(message: Message, state: FSMContext):
    try:
        await state.update_data(night_hours=message.text)
        await state.set_state(Shift.date)
        await message.reply("Вкажіть дату: \n"
                            "Введіть дату у наступному форматі: \n"
                            "*Рік/Місяць/День* \n"
                            "Приклад: 2015/10/20",
                            reply_markup=today_btn,
                            parse_mode="MARKDOWN")
    except ValueError:
        await state.clear()
        await message.reply('Помилка! Введіть число🛑',
                            reply_markup=admin_kb_main)


@admin_router.message(Shift.date)
async def process_simple_calendar(message: Message, state: FSMContext):
    try:
        if message.text.lower() == "Сьогоднішня дата":
            cur_date = date.today()#.strftime("%Y/%m/%d")
        else:
            cur_date = datetime.strptime(message.text, "%Y/%m/%d").date()
        await state.update_data(date=cur_date)
        data = await state.get_data()
        create_shift(data)
        await message.reply('Ви додали нову зміну!',
                            reply_markup=admin_kb_main)
    except Exception as err:
        logger.error(err)
        await message.reply("Не вірний формат!",
                            reply_markup=admin_kb_main)
    finally:
        await state.clear()





