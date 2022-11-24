
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import BaseFilter
from aiogram.types import Message

from DataBase.base import redis_just_one_read
from loader import all_data

data = all_data()
bot = data.get_bot()


class IsDriver(BaseFilter):

    async def __call__(self, message: Message) -> bool:
        try:
            status = await redis_just_one_read(f"User: Status_delivery: {message.from_user.id}")

            user_channel_status = await bot.get_chat_member(chat_id=data.driver_group, user_id=message.from_user.id)

            if user_channel_status.status != 'left':
                if status is None:
                    return True
                if status == '0':
                    return True
                if status == '1':
                    if message.text != "Я приехал":
                        await bot.send_message(chat_id=message.from_user.id,
                                               text='Вы не можете перейти в меню, пока не завершите поездку.')
                        return False
            else:
                return False
        except TelegramBadRequest:
            await bot.send_message(message.from_user.id, 'Только подписчики канала могут пользоваться ботом')
            return False