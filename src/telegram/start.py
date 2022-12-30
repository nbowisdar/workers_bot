from aiogram import Dispatcher
# from src.telegram.handlers.admin import admin_router
from src.telegram.setup import bot
from src.telegram.handlers import admin_router
from src.telegram.handlers import user_router
from src.telegram.handlers import common_router


async def start_bot():
    dp = Dispatcher()
    dp.include_router(common_router)
    dp.include_router(admin_router)
    dp.include_router(user_router)
    await dp.start_polling(bot)

