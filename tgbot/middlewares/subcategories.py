from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.types import Message

from tgbot.misc.backend import Item


class SubCategoriesMiddleware(BaseMiddleware):
    async def on_pre_process_message(self, message: Message, data: dict):
        try:
            _ = data["subcategories"]
        except KeyError:
            api: Item = message.bot.get("items_api")
            categories = await api.get_categories()
            subcategories = []
            for category in categories:
                subcategories.extend(
                    await api.get_subcategories(category["code"])
                )
            data["subcategories"] = [elem["code"] for elem in subcategories]
