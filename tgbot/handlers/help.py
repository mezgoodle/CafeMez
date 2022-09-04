from aiogram.types import Message
from aiogram.dispatcher.filters import CommandHelp, Command

from loader import dp


@dp.message_handler(Command('courier_help'), state='*', is_courier=True)
async def courier_help_command(message: Message) -> Message:
    return await message.reply('Вітаємо! Ви повинні брати замовлення зі списку та змінювати статус доставки.\n\n'
                               'Щоб почати користуватись ботом, ви можете:\n'
                               '* /orders - показати усі замовлення вашого ресторану\n'
                               '* /my_order - показати замовлення, що ви узяли')


@dp.message_handler(Command('chef_help'), state='*', is_chef=True)
async def chef_help_command(message: Message) -> Message:
    return await message.reply('Вітаємо! Ви повинні керувати готовністю замовлень у вашому ресторані.\n\n'
                               'Щоб почати користуватись ботом, ви можете:\n'
                               '* /orders - показати усі замовлення вашого ресторану\n')


@dp.message_handler(Command('admin_help'), state='*', is_admin=True)
async def admin_help_command(message: Message) -> Message:
    return await message.reply('Вітаємо! Ви повинні керувати замовленнями, '
                               'місцями у ресторані та виконувати адміністративну роботу.\n\n'
                               'Щоб почати користуватись ботом, ви можете:\n'
                               '* /orders - показати усі замовлення вашого ресторану\n'
                               '* /rs - видалити ресторан\n'
                               '* /add_rs - додати ресторан\n'
                               '* /places - змінити доступність місць у ресторані\n'
                               '* /tell_everyone - зробити повідомлення усім користувачам\n')


@dp.message_handler(CommandHelp(), state='*')
async def help_command(message: Message) -> Message:
    return await message.reply('Вітаємо! Щоб почати користуватись ботом, ви можете:\n'
                               '* /places - забронювати місце\n'
                               '* /menu - відкрити меню\n'
                               '* /cart - відкрити корзину\n'
                               '* /rs - знайти найближчий ресторан\n'
                               '* /faq - часті питання та відповіді\n'
                               '* /my_ref - створити реферальне посилання\n'
                               '* /admin_help - список команд для адміністратора\n'
                               '* /chef_help - список команд для шеф-кухара\n'
                               '* /courier_help - список команд для кур\'єра\n\n'
                               'Якщо вас цікавить робота в ресторані, зверніться до @sylvenis.')
