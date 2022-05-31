from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from tgbot.utils import database


class ACLMiddleware(BaseMiddleware):
    def __init__(self):
        super(ACLMiddleware, self).__init__()

    @staticmethod
    async def setup_chat(data: dict, user_data: types.User):
        user_id = user_data.id

        user = database.get_user(user_id)
        data['user'] = user

    async def on_pre_process_message(self, message: types.Message, data: dict):
        await self.setup_chat(data, message.from_user)

    async def on_pre_process_callback_query(self, query: types.CallbackQuery, data: dict):
        await self.setup_chat(data, query.from_user)
