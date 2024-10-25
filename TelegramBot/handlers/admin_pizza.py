from aiogram import Router, F, types
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from bot_config import database


class PizzaReview(StatesGroup):
    name_food = State()
    price = State()
    category_food = State()
    confirm = State()

admin = 5690761577
admin_pizza_router = Router()
admin_pizza_router.message.filter(F.from_user.id == admin)

@admin_pizza_router.message(Command("newfood"))
async def start_food_form(message: types.Message, state: FSMContext):
    await state.set_state(PizzaReview.name_food)
    await message.answer("Задайте название блюда:")

@admin_pizza_router.message(PizzaReview.name_food)
async def procces_name_food(message: types.Message, state: FSMContext):
    await state.update_data(name_food=message.text)
    await state.set_state(PizzaReview.price)
    await message.answer("Задайте цену блюда:")


@admin_pizza_router.message(PizzaReview.price)
async def procces_price(message: types.Message, state: FSMContext):
    await state.update_data(price=message.text)
    await state.set_state(PizzaReview.category_food)
    await message.answer("Выберите категорию блюда (Пиццы, Закуски, Напитки, Десерты, Соусы):")

@admin_pizza_router.message(PizzaReview.category_food)
async def procces_category_food(message: types.Message, state: FSMContext):
    await state.update_data(category_food=message.text)
    data = await state.get_data()
    kb = types.ReplyKeyboardMarkup(
        keyboard=[[
            types.KeyboardButton(text="Да"),
            types.KeyboardButton(text="Нет")
        ]],
        resize_keyboard=True
    )
    await state.set_state(PizzaReview.confirm)
    await message.answer(f"Вы ввели:\n Название: {data['name_food']},\n Цена: {data['price']},\n "
                         f"Категория: {data['category_food']}", reply_markup=kb)

@admin_pizza_router.message(PizzaReview.confirm, F.text == "Да")
async def procces_confirm(message: types.Message, state: FSMContext):
    data = await state.get_data()
    print(data)
    database.execute(
        query="""
        INSERT INTO dishes (name_food, price, category_food)
        VALUES (?, ?, ?)
        """,
        params=(
            data['name_food'],
            data['price'],
            data['category_food']
        )
    )
    await state.clear()
    kb = types.ReplyKeyboardRemove()
    await message.answer("Данные были сохранены!", reply_markup=kb)


@admin_pizza_router.message(PizzaReview.confirm, F.text == 'Нет')
async def procces_not_confirmed(message: types.Message, state: FSMContext):
    await state.set_state(PizzaReview.name_food)
    await message.answer("Задайте название блюда:")