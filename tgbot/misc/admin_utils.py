from typing import Tuple

from aiogram.dispatcher.filters import Command
from aiogram.types import Message
from aiogram.utils.markdown import hbold, hitalic

from tgbot.states.states import User


def check_username(command: Command.CommandObj) -> Tuple[bool, str]:
    """Function for checking right writing of nickname

    Args:
        command (Command.CommandObj): telegram message with nickname object

    Returns:
        Tuple[bool, str]: boolean value, if nickname was written right, and reason or username itself
    """
    try:
        username: str = command.args.split(" ")[0]
    except (TypeError, AttributeError):
        return (
            False,
            f'Потрібно вказати {hitalic("nickname")} користувача. Приклад: /add_admin @username',
        )
    if not username.startswith("@"):
        return False, f'Нікнейм повинен писатись як {hbold("@" + username)}'
    return True, username[1:]


async def start_registration(message: Message) -> Message:
    """Just common logic for registration

    Args:
        message (Message): message from the telegram

    Returns:
        Message: message from the bot
    """
    await User.first()
    return await message.answer(
        "Перешліть будь ласка повідомлення від користувача, якого ви хочете додати в базу даних.\n"
        f'{hbold("Уважно перегляньте налаштування приватності!")}'
    )
