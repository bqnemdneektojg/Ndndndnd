from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import Message
from aiogram.dispatcher.filters import BoundFilter

class CellarImport(StatesGroup):
	rasst = State()

class dialog(StatesGroup):
    spam = State()

class linkTamer(StatesGroup):
    text = State()

class IsPrivate(BoundFilter):
    async def check(self, message: types.Message):
        return message.chat.type == types.ChatType.PRIVATE