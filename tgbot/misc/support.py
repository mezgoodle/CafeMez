from typing import Optional
from random import shuffle

from aiogram import Bot

from tgbot.misc.backend import User
from loader import dp


async def check_support_available(support_id) -> Optional[int]:
    state = dp.current_state(chat=support_id, user=support_id)
    state_str = str(await state.get_state())
    if state_str == 'in_support':
        return None
    else:
        return support_id


async def get_support_manager() -> int:
    bot: Bot = Bot.get_current()
    api: User = bot.get('users_api')
    users = await api.get_staff()
    shuffle(users)
    for user in users:
        if support_id := await check_support_available(user['telegram_id']):
            return support_id
    else:
        return
