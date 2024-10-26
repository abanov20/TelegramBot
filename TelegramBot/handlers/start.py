from aiogram import Router, F, types
from aiogram.filters.command import Command

from bot_config import database


start_router = Router()

@start_router.message(Command('start'))
async def command_start(message: types.Message):
    user_id = message.from_user.id
    name = message.from_user.first_name

    check_user = database.execute(
        query="SELECT * FROM users WHERE tg_id = ?",
        params=(user_id,)
    ).fetchone()

    print(check_user)
    if check_user is None:
        database.execute(
            query="INSERT INTO users (tg_id, first_name) VALUES (?, ?)",
            params=(user_id, name)
        )

    total_user = database.execute(
        query="SELECT COUNT(*) FROM users WHERE tg_id = ?",
        params=(user_id,)
    ).fetchone()

    kb = types.InlineKeyboardMarkup(
        inline_keyboard=[
            [
                types.InlineKeyboardButton(
                    text="Наш сайт",
                    url="https://dodopizza.kg/bishkek"
                ),
                types.InlineKeyboardButton(
                    text="О нас",
                    callback_data="aboutus"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Наши адреса",
                    callback_data="ouraddress"
                ),
                types.InlineKeyboardButton(
                    text="Контакты",
                    callback_data="contacts"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Наш инстаграм",
                    url="https://www.instagram.com/dodopizzakg/"
                ),
                types.InlineKeyboardButton(
                    text="Наши вакансии",
                    callback_data="vacancies"
                )
            ],
            [
                types.InlineKeyboardButton(
                    text="Оставить отзыв",
                    callback_data="review"
                )
            ]
        ]

    )
    await message.reply(
        f'Привет {name}, наш бот обслуживает уже {total_user} пользователей!',
        reply_markup=kb
    )

@start_router.callback_query(F.data == "aboutus")
async def about_us_handler(callback: types.CallbackQuery):
    text = ("О НАС\n"
            "Обычно люди приходят в Додо Пиццу, чтобы просто поесть. Наши промоутеры раздают листовки про кусочек пиццы  или ещё что-то выгодное. Мы делаем это как первый шаг, чтобы познакомиться."
            "Но для нас Додо — не только пицца. Это и пицца тоже, но в первую очередь это большое дело, которое вдохновляет нас, заставляет каждое утро просыпаться и с интересом продолжать работу."
    )
    await callback.message.answer(text)

@start_router.callback_query(F.data == "ouraddress")
async def out_address_handler(callback: types.CallbackQuery):
    text = ("АДРЕСА:\n"
            "мкрн.Кок-жар 5/1.\n"
            "ул.Нуркамал Жетикашкаевой 29\n"
            "ул.Байтик Баатыра 96\n"
            "пр-т Чуйский 32Б\n"
            "ул. Фрунзе 37\n"
            "пр-т Чынгыза Айтматова 299в\n"
            "ул.Д.Шопокова 101/1\n"
            "ул.Б.Юнусалиева 179/2\n"
            "Пн-Вс: с 08:00 - до 01:00\n"
            "пр-т Манаса 7 Пн-Ср: с 08:00 - до 23:00\n"
            "Чт: с 08:00 до 23:30, Пт-Вс: с 08:00 - до 23:00\n"
            "ТРЦ<<I-Mall>> пер.Шевчеенко 80: Круглосуточно")
    await callback.message.answer(text)

@start_router.callback_query(F.data == "contacts")
async def contacts(callback: types.CallbackQuery):
    text = ("Контакты\n"
        "(551)550-550")
    await callback.message.answer(text)

@start_router.callback_query(F.data == "vacancies")
async def vacancies(callback: types.CallbackQuery):
    text = ("Хочешь есть пиццу бесплатно на обед?\n"
            "Ищем курьеров от 50000сом в месяц\n"
            "Ищем пиццамейкеров\n"
            "Ищем кассиров")
    await callback.message.answer(text)

