from aiogram.dispatcher.filters.state import StatesGroup, State


class User(StatesGroup):
    credentials = State()
    password = State()
    restaurant = State()
    email = State()


class Item(StatesGroup):
    name = State()
    price = State()
    description = State()
    photo = State()
    subcategory = State()
    approval = State()


class Mailing(StatesGroup):
    text = State()
