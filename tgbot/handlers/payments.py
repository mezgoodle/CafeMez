from aiogram import Bot
from aiogram.types import PreCheckoutQuery, ContentType, Message

from loader import dp
from tgbot.misc.payments import handle_place_payment, handle_order_payment
from tgbot.misc.backend import User
from tgbot.misc.referral import increase_referred


@dp.pre_checkout_query_handler()
async def pre_checkout(query: PreCheckoutQuery):
    bot: Bot = query.bot
    payload_data = query.invoice_payload.split(':')
    if query.order_info:
        email = query.order_info['email']
        api: User = bot.get('users_api')
        _, status = await api.create_user(query.from_user.username, email, query.from_user.id)
        if status != 201:
            return await bot.send_message(query.from_user.id, 'Виникла помилка. Зверніться до служби підтримки')
    payment_handlers = {
        'place': handle_place_payment,
        'order': handle_order_payment,
    }
    return await payment_handlers[payload_data[0]](query, payload_data, query.from_user.username)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: Message):
    await increase_referred(message)
    return await message.answer('Оплата теж успішна! Не видаляйте чек. Вам необхідно показати його у ресторані!')
