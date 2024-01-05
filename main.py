from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor
import motor.motor_asyncio as mt
from datetime import datetime

API_TOKEN = 'BOT_TOKEN'

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


clinet = mt.AsyncIOMotorClient('MONGODB_LINK')
collection = clinet.DB_Moder.Collection_Moder_bot


async def add_user(user_id, name):
    date = datetime.now().date()
    collection.insert_one({
        '_id': user_id,
        'name': name,
        'date': str(date)
    })



@dp.message_handler(content_types=types.ContentType.NEW_CHAT_MEMBERS)
async def delete_join_message(message: types.Message):
    await message.delete()

@dp.message_handler(content_types=types.ContentType.LEFT_CHAT_MEMBER)
async def delete_left_message(message: types.Message):
    await message.delete()

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    name = message.from_user.first_name
    await message.reply(f"Привет {name}! Я бот, который удаляет уведомления о вступлении и выходе из группы, а также о закреплении сообщений. Добавь меня в группу и предоставь права админа")
    user_id = message.from_user.id
    await add_user(user_id, name)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
