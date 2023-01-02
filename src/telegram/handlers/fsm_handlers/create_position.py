from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from src.database import get_all_workers_id
from src.schema import PositionModel
from src.telegram.keyboards import admin_kb_main
from src.telegram.setup import admin_router


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
    await message.reply("Вкажіть KPI позиції. (Приклад: 30 або 30.5)")


@admin_router.message(PositionState.kpi)
async def set_kpi_pos(message: Message, state: FSMContext):
    # all_workers_id = get_all_workers_id()
    kpi = message.text
    try:
        await state.update_data(лзш=float(kpi))
        await state.set_state(PositionState.wage_day)
        await message.reply("Вкажіть вартість часу у день")
    except ValueError:
        await message.reply(f"Невірне значення: *{kpi}*, повинно бути чило!",
                            reply_markup=admin_kb_main,
                            parse_mode="MARKDOWN")
        await state.clear()


@admin_router.message(PositionState.kpi)
async def set_day(message: Message, state: FSMContext):
    # all_workers_id = get_all_workers_id()
    wage = message.text
    try:
        await state.update_data(wage_day=float(wage))
        await state.set_state(PositionState.wage_night)
        await message.reply("Вкажіть вартість часу у день")
    except ValueError:
        await message.reply(f"Невірне значення: *{wage}*, повинно бути чило!",
                            reply_markup=admin_kb_main,
                            parse_mode="MARKDOWN")
        await state.clear()


@admin_router.message(PositionState.kpi)
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
    pass