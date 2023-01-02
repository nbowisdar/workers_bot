from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from src.database import get_all_workers_id, create_position
from src.schema import PositionModel
from src.telegram.keyboards import admin_kb_main
from src.telegram.setup import admin_router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

kpi30_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="30")]], resize_keyboard=True)


class PositionState(StatesGroup):
    name = State()
    kpi = State()
    # skill = State()
    wage_day = State()
    wage_night = State()


@admin_router.message(PositionState.name)
async def set_name_pos(message: Message, state: FSMContext):
    # all_workers_id = get_all_workers_id()

    await state.update_data(name=message.text)
    await state.set_state(PositionState.kpi)
    await message.reply("Вкажіть KPI позиції. (Приклад: 30 або 30.5)",
                        reply_markup=kpi30_kb)


@admin_router.message(PositionState.kpi)
async def set_kpi_pos(message: Message, state: FSMContext):
    # all_workers_id = get_all_workers_id()
    kpi = message.text
    try:
        await state.update_data(kpi=float(kpi))
        await state.set_state(PositionState.wage_day)
        await message.reply("Вкажіть вартість часу у день", reply_markup=ReplyKeyboardRemove())
    except ValueError:
        await message.reply(f"Невірне значення: *{kpi}*, повинно бути чило!",
                            reply_markup=admin_kb_main,
                            parse_mode="MARKDOWN")
        await state.clear()


@admin_router.message(PositionState.wage_day)
async def set_day(message: Message, state: FSMContext):
    # all_workers_id = get_all_workers_id()
    wage = message.text
    try:
        await state.update_data(wage_day=float(wage))
        await state.set_state(PositionState.wage_night)
        await message.reply("Вкажіть вартість часу у ноч")
    except ValueError:
        await message.reply(f"Невірне значення: *{wage}*, повинно бути чило!",
                            reply_markup=admin_kb_main,
                            parse_mode="MARKDOWN")
        await state.clear()


@admin_router.message(PositionState.wage_night)
async def set_night(message: Message, state: FSMContext):
    # all_workers_id = get_all_workers_id()
    wage = message.text
    try:
        await state.update_data(wage_night=float(wage))
        data = await state.get_data()
        await state.clear()
        await save_data(message, PositionModel(**data))

    except ValueError:
        await message.reply(f"Невірне значення: *{wage}*, повинно бути чило!",
                            reply_markup=admin_kb_main,
                            parse_mode="MARKDOWN")
        await state.clear()


async def save_data(message: Message, data: PositionModel):
    create_position(data)

    await message.answer(f"Ви створили нову позицію!\n"
                         f"Назва: *{data['name']}*\n"
                         f"KPI: *{data['kpi']}*\n"
                         f"Оплата день: *{data['wage_day']}* грн.\n"
                         f"Оплата ніч: *{data['wage_night']}* грн.",
                         reply_markup=admin_kb_main,
                         parse_mode="MARKDOWN")