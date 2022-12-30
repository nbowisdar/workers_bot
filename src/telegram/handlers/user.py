from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.filters import Text
from src.database import get_user
from src.telegram.handlers.fsm_handlers.show_wage_by_month import UserDate
from src.telegram.keyboards import start_kb, user_main_kb, user_emp_date, user_information, choose_information_btn, \
    get_years_kb
from src.telegram.messages import generate_message_with_user_info, generate_message_with_emp_date, generate_message_with_information, generate_message_general_information
from src.telegram.setup import user_router


@user_router.message(Text(text='Я працівник👷‍♂️'))
async def show_user_info(message: Message):
    try:
        user = get_user(message.from_user.id)
        await message.answer("Привіт, ви у розділі працівника",
                             reply_markup=user_main_kb)
    except AttributeError:
        await message.answer('Не можу знайти інформацію про вас👐', reply_markup=start_kb)


@user_router.message(Text(text="Мій профіль"))
async def my_profile(message: Message):
    user = get_user(message.from_user.id)
    msg = generate_message_with_user_info(user)
    await message.answer(msg, reply_markup=user_main_kb)


@user_router.message(Text(text="Заробітня плата"))
async def my_profile(message: Message, state: FSMContext):
    # user = get_user(message.from_user.id)
    await state.set_state(UserDate.year)
    await message.reply("Оберіть рік", reply_markup=get_years_kb())


@user_router.message(Text(text="Загальна інформація"))
async def my_profile(message: Message):
    user = get_user(message.from_user.id)
    msg = generate_message_with_information(user)
    await message.answer(msg, reply_markup=choose_information_btn)

@user_router.message(Text(text="Структура компанії"))
async def my_profile(message: Message):
    user = get_user(message.from_user.id)
    msg = generate_message_general_information(user)
    await message.answer(msg, reply_markup=user_information)