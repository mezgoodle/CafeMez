from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter

from tgbot.misc.backend import User


class IsChefFilter(BoundFilter):
    key = 'is_chef'

    def __init__(self, is_chef):
        self.is_chef = is_chef

    async def check(self, message: Message):
        api: User = message.bot['users_api']
        username = message.from_user.username
        return await api.is_job(username, 'is_chef')
