from aiogram import Router, F, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
import sqlite3

from bot_config import database

review_router = Router()

class PizzaReview(StatesGroup):
    name = State()
    phone_number = State()
    visit_date = State()
    food_rating = State()
    cleanliness_rating = State()
    extra_comments = State()

@review_router.callback_query(F.data == "review")
async def start_review_handler(callback: types.CallbackQuery, state: FSMContext):
    await state.set_state(PizzaReview.name)
    await callback.message.answer("Как Вас зовут?")

@review_router.message(PizzaReview.name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(PizzaReview.phone_number)
    await message.answer("Ваш номер телефона?")

@review_router.message(PizzaReview.phone_number)
async def procces_phone_number(message: types.Message, state: FSMContext):
    await state.update_data(phone_number=message.text)
    await state.set_state(PizzaReview.visit_date)
    await message.answer("Дата вашего посещения нашего заведения")

@review_router.message(PizzaReview.visit_date)
async def procces_food_rating(message: types.Message, state: FSMContext):
    await state.update_data(visit_date=message.text)
    await state.set_state(PizzaReview.food_rating)
    kb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
                types.KeyboardButton(text="1"),
                types.KeyboardButton(text="2"),
                types.KeyboardButton(text="3"),
                types.KeyboardButton(text="4"),
                types.KeyboardButton(text="5")
            ]
        ],
        resize_keyboard=True,
    )
    await message.answer("Качество еды", reply_markup=kb)

@review_router.message(PizzaReview.food_rating)
async def proccesing_cleanliness_rating(message: types.Message, state: FSMContext):
    await state.update_data(food_rating=message.text)
    await state.set_state(PizzaReview.cleanliness_rating)
    ckb = types.ReplyKeyboardMarkup(
        keyboard=[
            [
            types.KeyboardButton(text="1"),
            types.KeyboardButton(text="2"),
            types.KeyboardButton(text="3"),
            types.KeyboardButton(text="4"),
            types.KeyboardButton(text="5")
            ]
        ],
        resize_keyboard=True
    )
    await message.answer("Чистота заведения", reply_markup=ckb)

    @review_router.message(PizzaReview.cleanliness_rating)
    async def process_extra_comments(message: types.Message, state: FSMContext):
        await state.update_data(cleanliness_rating=message.text)
        await state.set_state(PizzaReview.extra_comments)
        await message.answer("Дополнительные комментарии или жалоба?")

@review_router.message(PizzaReview.extra_comments)
async def process_comment(message: types.Message, state: FSMContext):
    await state.update_data(extra_comments=message.text)
    data = await state.get_data()

    database.execute(
        query="""
            INSERT INTO review (name, phone_number, visit_date, food_rating, cleanliness_rating, comment)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
        params=(
            data['name'],
            data['phone_number'],
            data['visit_date'],
            data['food_rating'],
            data['cleanliness_rating'],
            message.text
        )
    )

    await message.answer(
        f"Спасибо за ваш отзыв, {data['name']}!\nВаш комментарий: {message.text}")
    await state.clear()