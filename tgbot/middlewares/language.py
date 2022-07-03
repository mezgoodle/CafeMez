from typing import Optional, Tuple, Any

from aiogram.types import User
from aiogram.contrib.middlewares.i18n import I18nMiddleware


async def get_lang(user_id: int) -> Optional[str]:
    return None


class ACLMiddleware(I18nMiddleware):
    async def get_user_locale(self, action: str, args: Tuple[Any]) -> Optional[str]:
        user = User.get_current()
        return await get_lang(user.id) or user.locale
