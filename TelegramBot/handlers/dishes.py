from aiogram import Router, types
from aiogram.filters import Command

from bot_config import database

dishes_catalog_router = Router()

@dishes_catalog_router.message(Command("dishes"))
async def dishes_catalog(message: types.Message):
    dishe = database.fetch(
        "SELECT * FROM dishes"
    )

    await message.answer("Католог наших блюд:")

    for dish in dishe:
        msg = f"Название: {dish['name_food']}\nЦены:{dish['price']}\nКатегория_еды: {dish['category_food']}"
        await message.answer(msg)