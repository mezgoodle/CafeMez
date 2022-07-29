from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter

from tgbot.misc.backend import User


class IsCourierFilter(BoundFilter):
    key = 'is_courier'

    def __init__(self, is_courier):
        self.is_courier = is_courier

    async def check(self, message: Message):
        api: User = message.bot['users_api']
        username = message.from_user.username
        return await api.is_job(username, 'is_courier')
