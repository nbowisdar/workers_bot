from aiogram import Bot, Router
from dotenv import load_dotenv
import os

load_dotenv()
TOKEN = os.getenv("TOKEN")
print(TOKEN)
bot = Bot(token=TOKEN)

# create routers
admin_router = Router()
user_router = Router()
common_router = Router()

# all admins

admins = [341769447, 132274199, 286365412]

