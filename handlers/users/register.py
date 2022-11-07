import asyncio
from datetime import datetime

from aiogram import Router
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from DataBase.base import sql_safe_insert, sql_safe_update
from filters.driver_filter import IsDriver
from states.driver_menu import Driver_menu
from states.driver_register import driver_reg

flags = {"throttling_key": "True"}
router = Router()
router.message(IsDriver())
router.message(state=driver_reg)

@router.message(state=driver_reg.name)
async def name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await state.set_state(driver_reg.car_number)
    await message.answer('Теперь напишите номер своего автомобиля в формате "A111AA11')

@router.message(state=driver_reg.car_number)
async def name(message: Message, state: FSMContext):
    number_car = message.text
    await state.update_data(number_car=number_car)
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="2.5Т"))
    nmarkup.row(types.KeyboardButton(text="5Т"))
    nmarkup.row(types.KeyboardButton(text="10Т"))
    await state.set_state(driver_reg.car_mass)
    await message.answer("Выберите вместимость вашего автомобиля, или напишите вес в формате: 10Т")

@router.message(state=driver_reg.car_mass)
async def name(message: Message, state: FSMContext):
    data = await state.get_data()
    car_mass = message.text
    await sql_safe_insert('users', {'user_id': message.from_user.id, 'username': data['name'],
                                    'DateTime_come': datetime.now(), 'car_number': data['number_car'],
                                    'car_mass': car_mass})
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="Мой кабинет"))
    await state.set_state(Driver_menu.main)
    await message.answer("Ваша регистрация прошла успешно, теперь вы можете получать заказы. \n\n"
                         "Вам будет приходить от меня уведомления о доступном заказе\n"
                         "Вы можете принять заказ и его выполнить или отказаться от него", reply_markup=nmarkup.as_markup(resize_keyboard=True))



