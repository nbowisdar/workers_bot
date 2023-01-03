from aiogram import F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Text, Command

from src.telegram.handlers.fsm_handlers.create_position import PositionState
from src.telegram.handlers.fsm_handlers.update_user import UpdateWorker
from src.telegram.keyboards import admin_kb_main, admin_kb_pos, choose_time_btn
from loguru import logger
from aiogram.fsm.context import FSMContext
from src.telegram.handlers.fsm_handlers import CreateWorker, Shift, DropUser
from src.telegram.messages import message_with_all_users, msg_with_positions
from src.telegram.setup import admin_router, admins, admins_hip
from src.telegram.keyboards import cancel_kb
from src.database import get_all_workers, get_all_position


def is_admin(worker_id: int) -> bool:
    if worker_id in admins:
        return True
    return False


async def denied(message: Message):
    await message.answer('🛑Вам не доступний цей розділ!🛑')


async def check_access(message: Message):
    if not is_admin(message.from_user.id):
        await denied(message)
        raise Exception('Have no access')


# @admin_router.message(Text(text="admin🧑‍💻"))
@admin_router.message(F.text.in_({"admin🧑‍💻", "На головну"}))
async def main(message: Message):
    try:
        await check_access(message)
        await message.answer('Ви в розіділі адміна', reply_markup=admin_kb_main)
    except:
        logger.error(f'User {message.from_user.id} tried use admin panel!')


@admin_router.message(Text(text="Додати нового працівника"))
async def create_user(message: Message, state: FSMContext):
    try:
        await check_access(message)
        await state.set_state(CreateWorker.worker_id)
        await message.reply("Введіть id нового працівника:", reply_markup=cancel_kb)
    except:
        logger.error(f'User {message.from_user.id} tried use admin panel!')


@admin_router.message(Text(text="Видалити працівника"))
async def delete_worker(message: Message, state: FSMContext):
    try:
        await check_access(message)
        await state.set_state(DropUser.worker_id)
        await message.reply("Введіть id працівника якого бажаєте видалити:\n", reply_markup=cancel_kb)
    except:
        logger.error(f'User {message.from_user.id} tried use admin panel!')


@admin_router.message(Text(text="Оновити інфармацію про працівника"))
async def update_worker(message: Message, state: FSMContext):
    try:
        await check_access(message)
        await state.set_state(UpdateWorker.worker_id)
        await message.reply("Введіть id працівника інформацію котрого бажаєте оновити:", reply_markup=cancel_kb)
    except:
        logger.error(f'User {message.from_user.id} tried use admin panel!')


@admin_router.message(Text(text="Додати нову зміну"))
async def create_new_shift(message: Message, state: FSMContext):
    try:
        await check_access(message)
        await state.set_state(Shift.worker_id)
        await message.reply("Введіть id працівника:", reply_markup=cancel_kb)
    except:
        logger.error(f'User {message.from_user.id} tried use admin panel!')


@admin_router.message(Text(text="Показати всіх"))
async def show_all_workers(message: Message):
    try:
        await check_access(message)
        users = get_all_workers()
        msg = message_with_all_users(users)
        await message.answer(msg,
                             reply_markup=admin_kb_main,
                             parse_mode="MARKDOWN")
    except Exception as err:
        logger.error(f'User {message.from_user.id} tried use admin panel!')
        logger.error(err)

#286365412
@admin_router.message(Text(text="Детальніше про працівника"))
async def get_worker_info(message: Message, state: FSMContext):
    try:
        await check_access(message)
        await message.answer("Статистика", reply_markup=choose_time_btn)
        await state.set_state()
    except:
        logger.error(f'User {message.from_user.id} tried use admin panel!')


@admin_router.message((F.text == "Посади") & (F.from_user.id.in_(admins_hip)))
async def position(message: Message):
    await check_access(message)
    await message.answer("Розділ: *Посади*",
                         reply_markup=admin_kb_pos,
                         parse_mode="MARKDOWN")


@admin_router.message((F.text == "Усі посади") & (F.from_user.id.in_(admins_hip)))
async def show_pos(message: Message):
    all_pos = get_all_position()
    if not all_pos:
        await message.answer("Ви ще не створили не однієї посади", reply_markup=admin_kb_pos)
        return
    msg = msg_with_positions(all_pos)
    await message.answer(msg, reply_markup=admin_kb_pos, parse_mode="MARKDOWN")


@admin_router.message((F.text == "Створити нову посаду") & (F.from_user.id.in_(admins_hip)))
async def create_pos(message: Message, state: FSMContext):
    try:
        await check_access(message)
        await state.set_state(PositionState.name)
        await message.answer("Введіть назву посади", reply_markup=cancel_kb)
    except:
        logger.error(f'User {message.from_user.id} tried use admin panel!')



# @admin_router.message(Command(commands='test'))
# async def test(message: Message):
#     await message.answer(
#         "`test`",
#
#     )