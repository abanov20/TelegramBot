import asyncio
import logging
from aiogram import Bot

from bot_config import bot, dp, database
from handlers.start import start_router
from handlers.myinfo import myinfo_router
from handlers.random import random_router
from handlers.review import review_router
from handlers.admin_pizza import admin_pizza_router
from handlers.dishes import dishes_catalog_router

async def on_startup(bot: Bot):
    print("Бот запустился")
    database.create_table()


async def main():
    dp.include_router(start_router)
    dp.include_router(myinfo_router)
    dp.include_router(random_router)
    dp.include_router(review_router)
    dp.include_router(admin_pizza_router)
    dp.include_router(dishes_catalog_router)

    dp.startup.register(on_startup)
    # запуск бота
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
