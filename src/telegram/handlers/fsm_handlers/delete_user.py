from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from src.database import get_user, drop_user
from src.telegram.keyboards import yes_or_no_kb, admin_kb_main
from src.telegram.setup import admin_router


class DropUser(StatesGroup):
    worker_id = State()
    confirm = State()


@admin_router.message(DropUser.worker_id)
async def find_user(message: Message, state: FSMContext):
    user = get_user(int(message.text))
    if not user:
        await state.clear()
        await message.reply("Працівник з таким id не існує",
                            reply_markup=admin_kb_main)
        return
    else:
        await state.update_data(worker_id=user['worker_id'])
        await state.set_state(DropUser.confirm)
        await message.reply('Ви впевненні що бажаєте видалити цього працівника?',
                            reply_markup=yes_or_no_kb)


@admin_router.message(DropUser.confirm)
async def drop(message: Message, state: FSMContext):
    if not message.text.lower() == 'так':
        await state.clear()
        await message.reply("Відміна", reply_markup=admin_kb_main)

    else:
        data = await state.get_data()
        await state.clear()
        worker_id = data['worker_id']
        drop_user(worker_id)
        await message.answer(f'{worker_id} - Працівника видалено',
                             reply_markup=admin_kb_main)
