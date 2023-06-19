from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from tgbot.misc.backend import User


class IsGeneralAdminFilter(BoundFilter):
    key = "is_general_admin"

    def __init__(self, is_general_admin):
        self.is_general_admin = is_general_admin

    async def check(self, message: Message):
        api: User = message.bot["users_api"]
        username = message.from_user.username
        return await api.is_job(username, "is_superuser")


class IsAdminFilter(BoundFilter):
    key = "is_admin"

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, message: Message):
        api: User = message.bot["users_api"]
        username = message.from_user.username
        return await api.is_job(username, "is_staff")
