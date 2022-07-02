from aiogram.dispatcher.filters.state import StatesGroup, State


class Admin(StatesGroup):
    username = State()
    password = State()
    email = State()
    telegram_id = State()
    is_staff = State()
