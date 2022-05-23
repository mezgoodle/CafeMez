from aiogram.dispatcher.filters import Command
from aiogram.utils.markdown import hbold, hitalic
from typing import Tuple


def check_nickname(command: Command.CommandObj) -> Tuple[bool, str]:
    try:
        username: str = command.args.split(' ')[0]
    except (TypeError, AttributeError):
        return False, f'Потрібно вказати {hitalic("nickname")} користувача. Приклад: /add_admin @username'
    if not username.startswith('@'):
        return False, f'Нікнейм повинен писатись як {hbold("@" + username)}'
    return True, f'Додано адміністратора {username}'
