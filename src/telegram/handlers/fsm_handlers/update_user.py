from pprint import pprint

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from src.telegram.handlers.fsm_handlers.create_user_fsm import get_pos_kb
from src.telegram.keyboards import next_kb
from src.database import create_worker, get_user, update_user, get_pos_by_name
from src.schema import UserModel
from src.telegram.keyboards import admin_kb_main
from src.telegram.setup import admin_router
from aiogram.filters import Text


class UpdateWorker(StatesGroup):
    worker_id = State()
    name = State()
    surname = State()
    phone = State()
    email = State()
    tag = State()
    department = State()
    position = State()
    status = State()
    #kpi = State()
    skill = State()
    #wage_day = State()
    #wage_night = State()
    note = State()
    employment_date = State()


async def get_user_from_state(state: FSMContext) -> UserModel:
    data = await state.get_data()
    worker_id = data['worker_id']
    return get_user(worker_id)


@admin_router.message(UpdateWorker.worker_id)
async def set_worker_id(message: Message, state: FSMContext):
    try:
        worker_id = int(message.text)
        user = get_user(worker_id)

        await state.update_data(worker_id=worker_id)
        await state.set_state(UpdateWorker.name)
        await message.reply("Вкажіть нове ім'я:\n"
                            f"Попереднє значення - {user['name']}",
                            reply_markup=next_kb)
    except ValueError:
        await wrong_input(message, state)


@admin_router.message(UpdateWorker.name)
async def set_name(message: Message, state: FSMContext):
    user = await get_user_from_state(state)
    if message.text.lower() == "далі (залишити як є)":
        await state.update_data(name=user['name'])
    else:
        await state.update_data(name=message.text)
    await state.set_state(UpdateWorker.surname)
    await message.reply("Вкажіть нове прізвище: \n"
                        f"Попереднє значення - {user['surname']}",
                        reply_markup=next_kb)


@admin_router.message(UpdateWorker.surname)
async def set_surname(message: Message, state: FSMContext):
    user = await get_user_from_state(state)
    if message.text.lower() == "далі (залишити як є)":
        await state.update_data(surname=user['surname'])
    else:
        await state.update_data(surname=message.text)
    await state.set_state(UpdateWorker.phone)
    await message.reply("Вкажіть новий телефон: \n"
                        f"Попереднє значення - {user['phone']}",
                        reply_markup=next_kb)


@admin_router.message(UpdateWorker.phone)
async def set_phone(message: Message, state: FSMContext):
    user = await get_user_from_state(state)
    if message.text.lower() == "далі (залишити як є)":
        await state.update_data(phone=user['phone'])
    else:
        await state.update_data(phone=message.text)
    await state.set_state(UpdateWorker.email)

    await message.reply("Вкажіть новий E-mail: \n"
                        f"Попереднє значення - {user['email']}",
                        reply_markup=next_kb)


@admin_router.message(UpdateWorker.email)
async def set_email(message: Message, state: FSMContext):
    user = await get_user_from_state(state)
    if message.text.lower() == "далі (залишити як є)":
        await state.update_data(email=user['email'])
    else:
        await state.update_data(email=message.text)
    await state.set_state(UpdateWorker.tag)

    await message.reply("Вкажіть новий телеграм тег: \n"
                        f"Попереднє значення - {user['tag']}",
                        reply_markup=next_kb)


@admin_router.message(UpdateWorker.tag)
async def set_tag(message: Message, state: FSMContext):
    user = await get_user_from_state(state)
    if message.text.lower() == "далі (залишити як є)":
        await state.update_data(tag=user['tag'])
    else:
        await state.update_data(tag=message.text)
    await state.set_state(UpdateWorker.department)

    await message.reply("Вкажіть новий відділ: \n"
                        f"Попереднє значення - {user['department']}",
                        reply_markup=next_kb)


@admin_router.message(UpdateWorker.department)
async def set_department(message: Message, state: FSMContext):
    user = await get_user_from_state(state)
    if message.text.lower() == "далі (залишити як є)":
        await state.update_data(department=user['department'])
    else:
        await state.update_data(department=message.text)
    await state.set_state(UpdateWorker.position)

    await message.reply("Вкажіть нову посаду: \n"
                        f"Попереднє значення - {user['position']['name']}",
                        reply_markup=get_pos_kb())


@admin_router.message(UpdateWorker.position)
async def set_position(message: Message, state: FSMContext):
    user = await get_user_from_state(state)
    if message.text.lower() == "далі (залишити як є)":
        await state.update_data(position=user['position'])
    else:
        await state.update_data(position=message.text)
    await state.set_state(UpdateWorker.status)

    await message.reply("Вкажіть новий статус працівника: \n"
                        f"Попереднє значення - {user['status']}",
                        reply_markup=next_kb)


@admin_router.message(UpdateWorker.status)
async def set_status(message: Message, state: FSMContext):
    user = await get_user_from_state(state)
    if message.text.lower() == "далі (залишити як є)":
        await state.update_data(status=user['status'])
    else:
        await state.update_data(status=message.text)
    await state.set_state(UpdateWorker.skill)

    await message.reply("Вкажіть рівень навичок працівника: \n"
                        f"Попереднє значення - {user['skill']}",
                        reply_markup=next_kb)


@admin_router.message(UpdateWorker.skill)
async def set_skill(message: Message, state: FSMContext):
    #try:
    user = await get_user_from_state(state)
    if message.text.lower() == "далі (залишити як є)":
        await state.update_data(skill=user['skill'])
    else:
        await state.update_data(skill=message.text)
    await state.set_state(UpdateWorker.employment_date)

    await message.reply("Вкажіть нову дата працевлаштування: \n"
                        f"Попереднє значення - {user['employment_date']}",
                        reply_markup=next_kb)


@admin_router.message(UpdateWorker.employment_date)
async def set_employment_date(message: Message, state: FSMContext):
    user = await get_user_from_state(state)
    if message.text.lower() == "далі (залишити як є)":
        await state.update_data(employment_date=user['employment_date'])
    else:
        await state.update_data(employment_date=message.text)
    await state.set_state(UpdateWorker.note)

    await message.reply("Оновити нотатку:\n"
                        f"Попереднє значення - {user['note']}",
                        reply_markup=next_kb)


@admin_router.message(UpdateWorker.note)
async def set_note(message: Message, state: FSMContext):
    user = await get_user_from_state(state)
    if message.text.lower() == "далі (залишити як є)":
        await state.update_data(note=user['note'])
    else:
        await state.update_data(note=message.text)
    data = await state.get_data()
    await state.clear()
    await save_data(message, data)


async def save_data(message: Message, data: dict):
    # data['day_plus_night'] = data['day'] + data['night']
    data["position"] = get_pos_by_name(data["position"])
    user = UserModel(**data)
    update_user(user)

    await message.reply("Оновлення даних усіпішне!",
                        reply_markup=admin_kb_main)


async def wrong_input(message: Message, state: FSMContext):
    await state.clear()
    wrong_chunk = message.text
    await message.reply(f'"{wrong_chunk}" - Не вірне значення!',
                        reply_markup=admin_kb_main)
