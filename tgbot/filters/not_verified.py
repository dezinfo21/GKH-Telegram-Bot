""" Not verified users only filter """
from dataclasses import dataclass

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from tgbot.services import database


@dataclass
class NotVerifiedUsersOnly(BoundFilter):
    """
    Handler filter to apply only for not verified users
    """
    key = "not_verified_only"
    not_verified_only: bool

    async def check(self, message: Message) -> bool:
        user = await database.get_user(message.from_user.id)

        return bool(user) is not self.not_verified_only
