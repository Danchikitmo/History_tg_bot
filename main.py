import asyncio
import logging

from aiogram import Bot
from aiogram import Dispatcher
from aiogram import types
from aiogram.client.default import DefaultBotProperties
# from aiogram.dispatcher import router
from aiogram.enums import ParseMode
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.storage.memory import MemoryStorage


import config
import dataBase.modal
from handlers import handler_admin_selection


async def main():
    from handlers import router
    await dataBase.modal.connect_db()
    bot = Bot(token=config.BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())

    handler_admin_selection(bot)



class UserForm_name(StatesGroup):
    waiting_for_name = State()

class UserForm_surname(StatesGroup):
    waiting_for_surname = State()






if __name__ == '__main__':
    asyncio.run(main())
