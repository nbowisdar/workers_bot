from pprint import pprint

from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from src.database import get_all_workers_id, create_position
from src.schema import PositionModel
from src.telegram.keyboards import admin_kb_main, admin_kb_pos
from src.telegram.other import extract_kpi_data, pars_kpi_data
from src.telegram.setup import admin_router
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
import json

kpi30_kb = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text="30")]], resize_keyboard=True)


class PositionState(StatesGroup):
    name = State()
    kpi = State()
    kpi_data = State()
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
        await state.set_state(PositionState.kpi_data)
        await message.reply("Вкажіть на які поля та % на які буде ділитяся KPI.\n"
                            "Данні повинні бути у такому форматі!\n"
                            "`поле1->5 поле2->5 поле3->20`\n"
                            "Де:  поле - назва одного з KPI\n"
                            "Значення - %\n"
                            "Пильнуйте щоби у вас вийшло 30%",
                            reply_markup=ReplyKeyboardRemove(),
                            parse_mode="MARKDOWN")
    except ValueError:
        await message.reply(f"Невірне значення: *{kpi}*, повинно бути чило!",
                            reply_markup=admin_kb_main,
                            parse_mode="MARKDOWN")
        await state.clear()


@admin_router.message(PositionState.kpi_data)
async def set_kpi_pos(message: Message, state: FSMContext):
    kpi_data = message.text
    try:
        parsed_data = pars_kpi_data(kpi_data, check_30_percent=True)
        await state.update_data(kpi_data=parsed_data)
        await state.set_state(PositionState.wage_day)
        await message.reply("Вкажіть вартість часу у день", reply_markup=ReplyKeyboardRemove())
    except Exception as err:
        await message.reply(f"Виникла наступна помилка - `{err}`",
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
        await message.reply("Вкажіть вартість часу у ночі")
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
    kpi_text_part = extract_kpi_data(data['kpi_data'])
    await message.answer(f"Ви створили нову позицію!\n"
                         f"Назва: *{data['name']}*\n"
                         f"KPI: *{data['kpi']}*\n"
                         f"{kpi_text_part}"
                         f"Оплата день: *{data['wage_day']}* грн.\n"
                         f"Оплата ніч: *{data['wage_night']}* грн.",
                         reply_markup=admin_kb_pos,
                         parse_mode="MARKDOWN")