from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from src.database import get_wage_data_by_month
from src.schema import YearMonth
from src.telegram.keyboards import user_main_kb, get_months_kb
from src.telegram.messages import build_month_wage_message
from src.telegram.other import get_num_month
from src.telegram.setup import common_router


class UserDate(StatesGroup):
    year = State()
    month = State()


@common_router.message(UserDate.year)
async def set_year(message: Message, state: FSMContext):
    await state.update_data(year=message.text)
    await message.answer("Вкажить за який місяць потрібні данні",
                         reply_markup=get_months_kb())
    await state.set_state(UserDate.month)


@common_router.message(UserDate.month)
async def set_year(message: Message, state: FSMContext):
    await state.update_data(month=message.text)
    data = await state.get_data()
    await state.clear()
    data["worker_id"] = message.from_user.id

    await _handle_data(data, message)


async def _handle_data(data: dict, message: Message):
    data["month"] = get_num_month(data["month"])
    wage_info = get_wage_data_by_month(YearMonth(**data))
    msg = build_month_wage_message(wage_info)
    await message.answer(msg, reply_markup=user_main_kb)

