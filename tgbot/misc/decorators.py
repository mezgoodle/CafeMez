from aiohttp import ClientConnectorError
from aiogram import Bot
from aiogram.types import User
from aiogram.utils.markdown import hbold

import logging
from functools import wraps


def api_decorator(method):
    logger = logging.getLogger(__name__)
    method_name = hbold(method.__name__)

    @wraps(method)
    async def wrapper(*args, **kwargs):
        bot = Bot.get_current()
        user_id = User.get_current().id
        try:
            return await method(*args, **kwargs)
        except ClientConnectorError:
            logger.error(f'Error in function {method_name}: Connection error')
            await bot.send_message(user_id, 'Помилка при з\'єднанні з сервером. Перевірте лог-файли.')
        except Exception:
            logger.error(f'Error in function {method_name}')
    return wrapper
