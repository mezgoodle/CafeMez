from aiogram.dispatcher.handler import CancelHandler
from aiogram.types import Message
from aiogram.dispatcher.middlewares import BaseMiddleware

from loader import dp


class SupportMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: Message, data: dict):
        state = dp.current_state(chat=message.from_user.id, user=message.from_user.id)
        state_str = str(await state.get_state())
        if state_str == 'in_support':
            data = await state.get_data()
            second_id = data.get('second_id')
            await message.copy_to(second_id)

            raise CancelHandler()
