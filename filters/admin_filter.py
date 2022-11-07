from aiogram.dispatcher.filters import BaseFilter
from aiogram.types import Message

from loader import all_data

data = all_data()


class IsAdmin(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        print(data.super_admins)
        print(message.from_user.id)
        if int(message.from_user.id) in data.super_admins:
            return True
        else:
            return False