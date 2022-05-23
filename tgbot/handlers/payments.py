from aiogram.types import PreCheckoutQuery

from loader import dp, bot


@dp.pre_checkout_query_handler()
async def pre_checkout(query: PreCheckoutQuery):
    print(query.order_info)
    await bot.answer_pre_checkout_query(query.id, ok=True)
    await bot.send_message(query.from_user.id, "Дякуємо за оренду!")
