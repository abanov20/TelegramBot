from aiogram import Router, types
from aiogram.filters import Command


random_router = Router()

@random_router.message(Command('random'))
async def send_random_pizza(message: types.Message):
    images_pizza = types.FSInputFile("images/кебаб.jpeg", "images/пеперони.jpeg")
    await message.answer_photo(
        photo=images_pizza,
        caption="Донерное мясо из говядины, моцарелла, томаты , красный лук , соленые огурчики , ранч соус, томатный соус",

    )
