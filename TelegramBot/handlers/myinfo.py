from aiogram import Router, F, types
from aiogram.filters.command import Command

myinfo_router = Router()

@myinfo_router.message(Command('myinfo'))
async def my_info(message: types.Message):
    user_id = message.from_user.id
    first_name = message.from_user.first_name
    user_name = message.from_user.username
    await message.answer(f'Ваш id:{user_id}, Имя:{first_name}, Имя_пользователя:{user_name}')
