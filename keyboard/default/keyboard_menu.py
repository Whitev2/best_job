from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

kb_menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text='Начать маршрут'),
        ],
        [
            KeyboardButton(text='Сделать заметку'),
            KeyboardButton(text='Какое то действие')
        ],
        [
            KeyboardButton(text='Завершить маршрут')
        ]
    ],
    resize_keyboard=True
)
