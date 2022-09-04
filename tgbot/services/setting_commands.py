from aiogram import Bot
from aiogram.types import BotCommand


async def set_default_commands(bot: Bot) -> None:
    commands = [
        BotCommand(command='start', description='Запустити бота'),
        BotCommand(command='help', description='Показати доступні команди'),
        BotCommand(command='admin_help', description='Показати доступні команди для адміністратора'),
        BotCommand(command='courier_help', description='Показати доступні команди для кур\'єра'),
        BotCommand(command='chef_help', description='Показати доступні команди для шеф-кухара'),
        BotCommand(command='rs', description='Знайти найближчий ресторан'),
        BotCommand(command='admin_rs', description='Знайти найближчий ресторан'),
        BotCommand(command='places', description='Забронювати місце у ресторані'),
        BotCommand(command='admin_places', description='Забронювати місце у ресторані'),
        BotCommand(command='my_ref', description='Отримати реферальне посилання'),
        BotCommand(command='menu', description='Відкрити меню'),
        BotCommand(command='cart', description='Показати корзину'),
        BotCommand(command='my_orders', description='Показати замовлення'),
        BotCommand(command='faq', description='Часті питання та відповіді'),
    ]
    await bot.set_my_commands(commands=commands)
