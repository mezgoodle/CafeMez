from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hitalic

from tgbot.states.states import User

from typing import Tuple


def check_username(command: Command.CommandObj) -> Tuple[bool, str]:
    try:
        username: str = command.args.split(' ')[0]
    except (TypeError, AttributeError):
        return False, f'Потрібно вказати {hitalic("nickname")} користувача. Приклад: /add_admin @username'
    if not username.startswith('@'):
        return False, f'Нікнейм повинен писатись як {hbold("@" + username)}'
    return True, username[1:]


async def start_registration(message: Message, command: Command.CommandObj, state: FSMContext):
    success, nickname = check_username(command)
    if success:
        await User.first()
        await state.update_data(username=nickname)
        await User.next()
        return await message.answer(f'Введіть пароль для користувача {nickname}')
    return await message.reply(nickname)
