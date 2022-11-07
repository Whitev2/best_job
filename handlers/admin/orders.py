import asyncio
import os
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from DataBase.base import sql_safe_insert, sql_safe_select, data_getter
from filters.admin_filter import IsAdmin
from handlers.users.start import admin_menu
from loader import all_data
from states.admin_states import Admin_state

router = Router()
router.message(state=Admin_state)
data = all_data()
bot = data.get_bot()

@router.message(F.text == 'Заказы')
async def orders(message: Message, state: FSMContext):
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="Малая (2.5 ТОННЫ < И > 5 ТОНН)"))
    nmarkup.row(types.KeyboardButton(text="Средняя (5 ТОНН)"))
    nmarkup.row(types.KeyboardButton(text="Большая (10 ТОНН)"))
    nmarkup.row(types.KeyboardButton(text="Возврат в меню"))
    await message.answer('Пожалуйста, выберите грузоподъёмность автомобиля', reply_markup=nmarkup.as_markup(resize_keyboard=True))

@router.message(F.text == 'Малая (2.5 ТОННЫ)')
async def orders(message: Message, state: FSMContext):
    request = await data_getter("SELECT * FROM users WHERE car_mass = '2.5Т'")
    await message.answer('Пожалуйста, выберите доступного водителя')
    if len(request) > 0:
        for driver in request:
            nmarkup = InlineKeyboardBuilder()
            nmarkup.button(text='Создать заказ', callback_data=f'{driver[0]}|new_order')
            print(driver)
            await message.answer(f'Водитель: {driver[1]}\nНомер автомобиля: {driver[-2]}', reply_markup=nmarkup.as_markup())
    else:
        await message.answer('Увы, водителей нет')

@router.message(F.text == 'Средняя (5 ТОНН)')
async def orders(message: Message, state: FSMContext):
    request = await data_getter("SELECT * FROM users WHERE car_mass = '5Т'")
    await message.answer('Пожалуйста, выберите доступного водителя')
    if len(request) > 0:
        for driver in request:
            nmarkup = InlineKeyboardBuilder()
            nmarkup.button(text='Создать заказ', callback_data=f'{driver[0]}|new_order')
            print(driver)
            await message.answer(f'Водитель: {driver[1]}\nНомер автомобиля: {driver[-2]}', reply_markup=nmarkup.as_markup())
    else:
        await message.answer('Увы, водителей нет')


@router.message(F.text == 'Большая (10 ТОНН)')
async def orders(message: Message, state: FSMContext):
    request = await data_getter("SELECT * FROM users WHERE car_mass = '10Т'")
    await message.answer('Пожалуйста, выберите доступного водителя')
    if len(request) > 0:
        for driver in request:
            nmarkup = InlineKeyboardBuilder()
            nmarkup.button(text='Создать заказ', callback_data=f'{driver[0]}|new_order')
            print(driver)
            await message.answer(f'Водитель: {driver[1]}\nНомер автомобиля: {driver[-2]}', reply_markup=nmarkup.as_markup())
    else:
        await message.answer('Увы, водителей нет')
