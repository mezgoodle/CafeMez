from aiogram.types import PreCheckoutQuery, ContentType, Message

from loader import dp
from tgbot.misc.payments import handle_place_payment, handle_order_payment


@dp.pre_checkout_query_handler()
async def pre_checkout(query: PreCheckoutQuery):
    payload_data = query.invoice_payload.split(':')
    payment_handlers = {
        'place': handle_place_payment,
        'order': handle_order_payment,
    }
    return await payment_handlers[payload_data[0]](query, payload_data, query.from_user.username)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_pay(message: Message):
    return await message.answer('Оплата теж успішна! Не видаляйте чек. Вам необхідно показати його у ресторані!')
