from aiogram.types import CallbackQuery
from aiogram.dispatcher.middlewares import BaseMiddleware


class CallbackMiddleware(BaseMiddleware):
    async def on_pre_process_callback_query(self, callback: CallbackQuery, data: dict):
        await callback.answer()
