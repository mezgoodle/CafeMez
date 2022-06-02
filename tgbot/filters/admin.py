from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter

from tgbot.config import Config, load_config


class IsGeneralAdminFilter(BoundFilter):
    key = 'is_general_admin'

    def __init__(self, is_general_admin):
        self.is_general_admin = is_general_admin

    async def check(self, message: Message):
        config: Config = load_config()
        return str(message.from_user.id) in config.tg_bot.admins


class IsAdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    # TODO: get admins from api
    async def check(self, message: Message):
        config: Config = load_config()
        return str(message.from_user.id) in config.tg_bot.admins
