from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.filters import Filter
from aiogram.types import Message, TelegramObject

ADMINS = [6083807927]


class AdminProtect(Filter):
    def __init__(self):
        self.admins = ADMINS

    async def __call__(self, message: Message):
        """Метод call вызывается автоматически"""
        return message.from_user.id in self.admins


class ExampleMiddleware(BaseMiddleware):
    async def __call__(self,
                       handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
                       event: TelegramObject, data: Dict[str, Any]
                       ) -> Any:
        """
        handler: сам объект хэндлера, который будет выполнен (или не выполнен при каком-то условии).
        event: тип Telegram-объекта, например Update, Message, CallbackQuery, InlineQuery.
        data: связанные данные, например FSM. Можем добавлять туда какие-то свои данные.
        """
        print('Actions before a handler')
        result = await handler(event, data)  # Start handler
        print('Actions after a handler')
        return result
