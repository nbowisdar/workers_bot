from pprint import pprint

from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, KeyboardButton
from src.telegram.keyboards import cancel_kb
from src.database import create_worker, get_all_workers_id, get_all_position, get_pos_by_name
from src.schema import UserModel
from src.telegram.keyboards import admin_kb_main
from src.telegram.setup import admin_router
from aiogram.filters import Text
from aiogram.utils.keyboard import KeyboardBuilder


class CreateWorker(StatesGroup):
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


@admin_router.message(Text(text="Відмінити"))
async def cancel_handler(message: Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.clear()
    await message.answer(
        "Відміна",
        reply_markup=admin_kb_main,
    )


@admin_router.message(CreateWorker.worker_id)
async def set_worker_id(message: Message, state: FSMContext):
    try:
        worker_id = int(message.text)
        if worker_id in get_all_workers_id():
            await message.reply("Працівник з цим id вже існує!",
                                reply_markup=admin_kb_main)
            await state.clear()
            return
        await state.update_data(worker_id=worker_id)
        await state.set_state(CreateWorker.name)
        await message.reply("Ім'я нового працівника:",
                            reply_markup=cancel_kb)
    except ValueError:
        await wrong_input(message, state)


@admin_router.message(CreateWorker.name)
async def set_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(CreateWorker.surname)
    await message.reply("Прізвище:",
                        reply_markup=cancel_kb)


@admin_router.message(CreateWorker.surname)
async def set_surname(message: Message, state: FSMContext):
    await state.update_data(surname=message.text)
    await state.set_state(CreateWorker.phone)
    await message.reply("Телефон:",
                        reply_markup=cancel_kb)


@admin_router.message(CreateWorker.phone)
async def set_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(CreateWorker.email)
    await message.reply("E-mail:",
                        reply_markup=cancel_kb)


@admin_router.message(CreateWorker.email)
async def set_email(message: Message, state: FSMContext):
    await state.update_data(email=message.text)
    await state.set_state(CreateWorker.tag)
    await message.reply("Телеграм тег:",
                        reply_markup=cancel_kb)


@admin_router.message(CreateWorker.tag)
async def set_tag(message: Message, state: FSMContext):
    await state.update_data(tag=message.text)
    await state.set_state(CreateWorker.department)
    await message.reply("Відділ:",
                        reply_markup=cancel_kb)


# create keyboards with relevant positions
def get_pos_kb():
    positions = get_all_position()
    builder = KeyboardBuilder(button_type=KeyboardButton)
    for pos in positions:
        builder.add(KeyboardButton(text=f"{pos['name']}"))
    builder.adjust(4)
    return builder.as_markup(resize_keyboard=True)


@admin_router.message(CreateWorker.department)
async def set_department(message: Message, state: FSMContext):
    await state.update_data(department=message.text)
    await state.set_state(CreateWorker.position)
    await message.reply("Посада:",
                        reply_markup=get_pos_kb())


@admin_router.message(CreateWorker.position)
async def set_position(message: Message, state: FSMContext):
    await state.update_data(position=message.text)
    await state.set_state(CreateWorker.status)
    await message.reply("Статус працівника:",
                        reply_markup=cancel_kb)


@admin_router.message(CreateWorker.status)
async def set_status(message: Message, state: FSMContext):
    await state.update_data(status=message.text)
    await state.set_state(CreateWorker.employment_date)
    await message.reply("Дата працевлаштування:",
                        reply_markup=cancel_kb)


# @admin_router.message(CreateWorker.kpi)
# async def set_kpi(message: Message, state: FSMContext):
#     await state.update_data(kpi=message.text)
#     await state.set_state(CreateWorker.skill)
#     await message.reply("Вкажіть рівень навичок робітника:",
#                         reply_markup=cancel_kb)

# @admin_router.message(CreateWorker.skill)
# async def set_skill(message: Message, state: FSMContext):
#     await state.update_data(skill=message.text)
#     await state.set_state(CreateWorker.employment_date)
#     await message.reply("Дата працевлаштування:",
#                         reply_markup=cancel_kb)


@admin_router.message(CreateWorker.employment_date)
async def set_employment_date(message: Message, state: FSMContext):
    await state.update_data(employment_date=message.text)
    await state.set_state(CreateWorker.note)
    await message.reply("Нотатка:",
                        reply_markup=cancel_kb)
#
# @admin_router.message(CreateWorker.wage_day)
# async def set_wage_day(message: Message, state: FSMContext):
#     await state.update_data(wage_day=message.text)
#     await state.set_state(CreateWorker.wage_night)
#     await message.reply("Ставка за нічні години:",
#                         reply_markup=cancel_kb)
#
#
# @admin_router.message(CreateWorker.wage_night)
# async def set_wage_night(message: Message, state: FSMContext):
#     await state.update_data(wage_night=message.text)
#     await state.set_state(CreateWorker.note)
#     await message.reply("Нотатка:",
#                         reply_markup=cancel_kb)


'''
@admin_router.message(CreateWorker.wage_day)
async def set_wage_day(message: Message, state: FSMContext):
    try:
        await state.update_data(wage_day=message.text)

    except ValueError:
        await message.reply("Невірне значення,\n"
                            "Наприклад: 50.5 або 50", reply_markup=admin_kb_main)
        await state.clear()
        await state.set_state(CreateWorker.wage_night)
        await message.reply("Ставка за нічні години:",
                        reply_markup=cancel_kb)

@admin_router.message(CreateWorker.wage_night)
async def set_wage_night(message: Message, state: FSMContext):
    try:
        await state.update_data(wage_night=message.text)

    except ValueError:
        await message.reply("Невірне значення,\n"
                            "Наприклад: 50.5 або 50", reply_markup=admin_kb_main)
        await state.clear()

'''


@admin_router.message(CreateWorker.note)
async def set_note(message: Message, state: FSMContext):
    await state.update_data(note=message.text)
    data = await state.get_data()
    await state.clear()
    await save_data(message, data)


async def save_data(message: Message, data: dict):
    # data['day_plus_night'] = data['day'] + data['night']
    data["position"] = get_pos_by_name(data["position"])
    user = UserModel(**data)
    create_worker(user)

    await message.reply("Ви додали нового працівника!",
                        reply_markup=admin_kb_main)


async def wrong_input(message: Message, state: FSMContext):
    await state.clear()
    wrong_chunk = message.text
    await message.reply(f'"{wrong_chunk}" - Не вірне значення!',
                        reply_markup=admin_kb_main)
