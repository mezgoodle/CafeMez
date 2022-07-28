from aiogram.dispatcher.filters.state import StatesGroup, State


class User(StatesGroup):
    credentials = State()
    password = State()
    email = State()


class Item(StatesGroup):
    name = State()
    price = State()
    description = State()
    photo = State()
    subcategory = State()


class Mailing(StatesGroup):
    text = State()
