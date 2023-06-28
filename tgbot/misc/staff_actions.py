from aiogram import Bot
from aiogram.types import CallbackQuery, Message
from aiogram.utils.markdown import hbold

from tgbot.keyboards.inline.orders import orders_keyboard
from tgbot.misc.backend import Order


async def show_orders_message(message: Message) -> Message:
    api: Order = message.bot.get("orders_api")
    orders = await api.get_orders(message.from_user.username)
    if orders:
        for order in orders:
            text = f'{hbold("Замовлення номер - ") + hbold(order["id"])}\n'
            keyboard = orders_keyboard(order)
            await message.answer(text, reply_markup=keyboard)
        return await message.answer(
            f'Щоб побачити деталі продукту - {hbold("натисніть на продукт")}\n'
            f'Щоб змінити статус замовлення - {hbold("натисніть на кнопку Готове або Не готове")}\n'
            f'Щоб змінити статус оплати - {hbold("натисніть на кнопку Оплачено або Не оплачено")}\n'
            f'Щоб видалити замовлення - {hbold("натисніть на кнопку Видалити")}'
        )
    return await message.answer("На даний момент немає замовлень")


async def show_item(callback_query: CallbackQuery, callback_data: dict):
    api: Order = callback_query.bot.get("orders_api")
    item = await api.get_order_item(callback_data["id"])
    text = (
        f'{hbold(item["item"]["name"])}\n'
        f'{hbold("Кількість:")} {item["quantity"]}\n'
        f'{hbold("Ціна за шт.:")} {item["item"]["price"]} грн.'
    )
    return await callback_query.message.answer_photo(
        photo=item["item"]["photo"], caption=text
    )


async def staff_action(
    callback_query: CallbackQuery,
    callback_data: dict,
    patch_data: dict,
    success_text: str,
    fail_text: str,
    need_check: bool = False,
    additional_text: str = None,
):
    api: Order = callback_query.bot.get("orders_api")
    bot: Bot = callback_query.bot
    if need_check:
        order = await api.get_order(callback_data["id"])
        if order["connected_courier"] != callback_query.from_user.username:
            return
    new_order, status = await api.update_order(callback_data["id"], patch_data)
    if status == 200:
        keyboard = orders_keyboard(new_order)
        if additional_text:
            await bot.send_message(
                new_order["user"]["telegram_id"], additional_text
            )
        await callback_query.message.answer(success_text)
        return await callback_query.message.edit_reply_markup(
            reply_markup=keyboard
        )
    return await callback_query.message.answer(fail_text)


async def finish_order_action(
    callback_query: CallbackQuery,
    callback_data: dict,
    success_text: str,
    fail_text: str,
    need_check: bool = False,
):
    api: Order = callback_query.bot.get("orders_api")
    if need_check:
        order = await api.get_order(callback_data["id"])
        if order["connected_courier"] != callback_query.from_user.username:
            return
    status = await api.finish_order(callback_data["id"])
    if status == 200:
        await callback_query.message.answer(success_text)
        return await callback_query.message.delete()
    return await callback_query.message.answer(fail_text)
