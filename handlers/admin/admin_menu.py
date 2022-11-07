import asyncio
import os
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from DataBase.base import sql_safe_insert
from filters.admin_filter import IsAdmin
from handlers.users.start import admin_menu
from loader import all_data
from states.admin_states import Admin_state

router = Router()
router.message(state=Admin_state)
data = all_data()
bot = data.get_bot()


@router.message(F.text == 'Управление ботом')
async def edit_bot(message: Message, state: FSMContext):
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="Редактировать текст"))
    nmarkup.row(types.KeyboardButton(text="Назад"))
    await message.answer('Выберите интересующий вас пункт меню', reply_markup=nmarkup.as_markup(resize_keyboard=True))

@router.message(F.text == 'Редактировать текст')
async def edit_text(message: Message, state: FSMContext):
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="Добавить текст"))
    nmarkup.row(types.KeyboardButton(text="Изменить текст"))
    nmarkup.row(types.KeyboardButton(text="Удалить текст"))
    nmarkup.row(types.KeyboardButton(text="Выйти"))
    await message.answer('Выберите интересующий вас пункт меню', reply_markup=nmarkup.as_markup(resize_keyboard=True))


"""********************************************* NEW TEXT **********************************************************"""

@router.message(F.text == 'Выйти', state=Admin_state.confirm_text)
async def confirm(message: Message, state: FSMContext):
    await state.clear()
    await admin_menu(message, state)

@router.message(F.text == 'Подтвердить', state=Admin_state.confirm_text)
async def confirm(message: Message, state: FSMContext):
    data = await state.get_data()
    state_name = await state.get_state()
    if state_name == 'Admin_state:confirm_text':
        tag = data['user_text'][0]
        text = data['user_text'][-1]
        await sql_safe_insert('texts', {'tag': tag, 'text': text})
        await message.answer('Текст успешно добавлен')
        await state.set_state(Admin_state.main_menu)
        await edit_text(message, state)


@router.message(F.text == 'Отменить', state=Admin_state.confirm_text)
async def confirm(message: Message, state: FSMContext):
    state_name = await state.get_state()
    if state_name == 'Admin_state:confirm_text':
        await message.answer('Отмена операции')
        await state.set_state(Admin_state.main_menu)
        await edit_text(message, state)


@router.message(F.text == 'Добавить текст')
async def add_text(message: Message, state: FSMContext):
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="Отменить"))
    await state.set_state(Admin_state.confirm_text)
    await message.answer('Пожалуйста напишите текст в формате: TAG|TEXT\n\nДопускается HTML-разметка', reply_markup=nmarkup.as_markup(resize_keyboard=True))


@router.message(state=Admin_state.confirm_text)
async def confirm_text(message: Message, state: FSMContext):
    user_text = message.html_text.split(sep='|')
    await state.update_data(user_text=user_text)
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="Подтвердить"))
    nmarkup.row(types.KeyboardButton(text="Отменить"))
    if len(user_text) == 2:
        await message.answer(f'Пожалуйста проверьте правильность введенных данных\n\n'
                             f'Тэг: {user_text[0]}\n\n'
                             f'Текст: {user_text[1]}', reply_markup=nmarkup.as_markup(resize_keyboard=True))
    else:
        await message.answer('Кажется вы не ввели тег или текст, пожалуйста повторите попытку',
                             reply_markup=nmarkup.as_markup(resize_keyboard=True))


@router.message(F.text == 'Изменить текст')
async def reset(message: Message, state: FSMContext):
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="Отменить"))

@router.message(F.text == 'Удалить текст')
async def reset(message: Message, state: FSMContext):
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="Отменить"))



