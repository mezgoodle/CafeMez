from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import CallbackQuery


class CallbackMiddleware(BaseMiddleware):
    async def on_pre_process_callback_query(
        self, callback: CallbackQuery, data: dict
    ):
        await callback.answer()
