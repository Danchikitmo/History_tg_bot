from aiogram import Bot
from aiogram.types import Message

import keyboard


async def notify_admin(bot: Bot, chat_id: str):
    await bot.send_message(chat_id=chat_id, text="Вы получили права администратора", reply_markup=keyboard.main_keyboard)


async def send_image_to_user(bot: Bot, chat_id: int, file_id: str):