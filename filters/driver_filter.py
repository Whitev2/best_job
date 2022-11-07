from aiogram.dispatcher.filters import BaseFilter
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message

from loader import all_data

data = all_data()
bot = data.get_bot()


class IsDriver(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        try:
            user_channel_status = await bot.get_chat_member(chat_id=data.driver_group, user_id=message.from_user.id)
            print(type(user_channel_status))
            if user_channel_status.status != 'left':
                return True
            else:
                await bot.send_message(message.from_user.id, 'Только подписчики канала могут пользоваться ботом')
                return False
        except TelegramBadRequest:
            await bot.send_message(message.from_user.id, 'Только подписчики канала могут пользоваться ботом')
            return False