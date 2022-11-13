from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def main_admin_keyboard():
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="Заказы"))
    nmarkup.row(types.KeyboardButton(text="Аналитика"))
    nmarkup.row(types.KeyboardButton(text="Управление ботом"))

    nmarkup.adjust(1, 1)
    return nmarkup.as_markup(resize_keyboard=True)