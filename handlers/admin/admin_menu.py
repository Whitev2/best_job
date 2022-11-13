import asyncio
import os
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, ReplyKeyboardRemove, InputFile, FSInputFile
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from DataBase.base import User
from filters.admin_filter import IsAdmin
from handlers.users.start import admin_menu
from loader import all_data
from states.admin_states import Admin_state
from xls_export.xls import export_to_xls

router = Router()
router.message(state=Admin_state)
data = all_data()
bot = data.get_bot()
user = User()


@router.message(F.text == 'Аналитика')
async def edit_bot(message: Message, state: FSMContext):
    if await export_to_xls():
        agenda = FSInputFile("xls_export/orders.xlsx", filename="orders.xlsx")
        await bot.send_document(chat_id=message.from_user.id, document=agenda)
    else:
        await message.answer("Не удалось отправить файл")

@router.message(F.text == 'Управление ботом')
async def edit_bot(message: Message, state: FSMContext):
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="Редактировать текст"))
    nmarkup.row(types.KeyboardButton(text="Управление водителями"))
    nmarkup.row(types.KeyboardButton(text="Назад"))
    await message.answer('Выберите интересующий вас пункт меню', reply_markup=nmarkup.as_markup(resize_keyboard=True))

@router.message(F.text == 'Выйти')
async def exit(message: Message, state: FSMContext):
    await edit_bot(message, state)

@router.message(F.text == 'Отмена')
async def exit(message: Message, state: FSMContext):
    await edit_bot(message, state)

@router.message(F.text == 'Назад')
async def exit(message: Message, state: FSMContext):
    await admin_menu(message, state)
@router.message(F.text == 'Редактировать текст')
async def edit_text(message: Message, state: FSMContext):
    await state.set_state(Admin_state.main_menu)
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="Добавить текст"))
    nmarkup.row(types.KeyboardButton(text="Изменить текст"))
    nmarkup.row(types.KeyboardButton(text="Удалить текст"))
    nmarkup.row(types.KeyboardButton(text="Выйти"))
    await message.answer('Выберите интересующий вас пункт меню', reply_markup=nmarkup.as_markup(resize_keyboard=True))

@router.message(F.text == 'Управление водителями')
async def driver_manage(message: Message, state: FSMContext):
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="Отмена"))
    await state.set_state(Admin_state.driver_edit)
    await message.answer("Напишите фио или номер автомобиля водителя",
                         reply_markup=nmarkup.as_markup(resize_keyboard=True))

@router.message(state=Admin_state.driver_edit)
async def driver_info(message: Message, state: FSMContext):
    user_info = await user.get_user({'car_number': message.text.lower()})
    if len(user_info) == 0:
        user_info = await user.get_user({'username': message.text.lower()})
    if len(user_info) != 0:
        nmarkup = InlineKeyboardBuilder()
        nmarkup.button(text='Рассчитать', callback_data=f'driver_calc|{user_info[0][0]}')
        nmarkup.button(text='Удалить из базы', callback_data=f'driver_del|{user_info[0][0]}')
        await message.answer(f"Водитель: {user_info[0][1].title()}\n"
                             f"Номер автомобиля: {user_info[0][3].upper()}\n"
                             f"Масса автомобиля: {user_info[0][5]}\n"
                             f"Зароботал: {user_info[0][4]}", reply_markup=nmarkup.as_markup())
    else:
        await message.answer("По данному запросу водитель не найден")

@router.callback_query(lambda call: 'driver_calc' in call.data)
async def driver_calc(query: types.CallbackQuery, state: FSMContext):
    data = query.data.split('|')
    driver_id = data[-1]
    await user.sql_update('users', {'balance': float(0)}, {'user_id': driver_id})
    await bot.send_message(chat_id=driver_id, text="Вам выдали зарплату, ваш текущий баланс был обнулён.")
    await query.message.answer('Вы успешно расчитали водителя')
    await edit_bot(query.message, state)





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
        await User.sql_safe_insert('texts', {'tag': tag, 'text': text})
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



