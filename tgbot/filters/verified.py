""" Verified users only filter """
from dataclasses import dataclass

from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from tgbot.services import database


@dataclass
class VerifiedUsersOnly(BoundFilter):
    """
    Handler filter to apply only for verified users
    """
    key = "verified_only"
    verified_only: bool

    async def check(self, message: Message) -> bool:
        user = await database.get_user(message.from_user.id)

        return bool(user) is self.verified_only
