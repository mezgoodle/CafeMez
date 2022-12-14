from aiogram.types import Message
from aiogram.dispatcher.filters.builtin import CommandStart, ChatTypeFilter
from aiogram.types import ChatType
from aiogram.utils.markdown import hbold

from loader import dp
from tgbot.misc.backend import Referral

from re import compile


@dp.message_handler(CommandStart(deep_link=compile(
    r'^[0-9]{3,15}$')), ChatTypeFilter(ChatType.PRIVATE))
async def register_referral(message: Message):
    referral = message.get_args()
    api: Referral = message.bot.get('referrals_api')
    _, status = await api.apply_referral(int(referral), message.from_user.id)
    if status == 201:
        return await message.answer(
            'Ви успішно зареєстрували чужий реферал. Щоб створити свій реферал, введіть команду /my_ref. '
            'Щоб побачити, як користуватись ботом, введіть команду /help')
    elif status == 400:
        return await message.answer(
            f'Невірний реферал. Можуть бути {hbold("дві помилки")}:\n'
            ' - Користувач, який надав реферал, не зареєстрований у системі.\n - Ви вже активовували реферал.')
    else:
        return await message.answer('Невідома помилка. Будь ласка, зверніться до адміністратора')


@dp.message_handler(CommandStart())
async def cmd_start(message: Message):
    return await message.answer('Вітаємо! Щоб побачити усі доступні команди, введіть команду:\n'
                                '* /help - для усіх користувачів\n'
                                '* /admin_help - для адміністраторів\n'
                                '* /chef_help - для шеф-кухарів\n'
                                '* /courier_help - для кур\'єрів\n')
