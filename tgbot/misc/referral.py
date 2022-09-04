from aiogram.types import Message

from tgbot.misc.backend import Referral, User


async def increase_referred(message: Message) -> None:
    refs_api: Referral = message.bot.get('referrals_api')
    users_api: User = message.bot.get('users_api')
    if data := await refs_api.get_referrer_parent(message.from_user.username):
        await users_api.increase_referred(data['username'], data['number'])
