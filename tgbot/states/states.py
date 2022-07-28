from aiogram.dispatcher.filters.state import StatesGroup, State


class User(StatesGroup):
    username = State()
    password = State()
    email = State()
    telegram_id = State()


class Item(StatesGroup):
    name = State()
    price = State()
    description = State()
    photo = State()
    subcategory = State()


class Mailing(StatesGroup):
    text = State()
