from typing import Union

from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove, ForceReply


async def simple_text(message: Message, tag: str,
                       reply_markup: Union[InlineKeyboardMarkup, ReplyKeyboardMarkup,
                                           ReplyKeyboardRemove, ForceReply, None] = None,
                       custom_caption: str = None):
    pass
