from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from tgbot.misc.backend import User


class IsRegisteredFilter(BoundFilter):
    key = "is_registered"

    def __init__(self, is_registered):
        self.is_registered = is_registered

    async def check(self, message: Message):
        api: User = message.bot["users_api"]
        username = message.from_user.username
        user = await api.get_user(username)
        return "detail" not in user.keys()
