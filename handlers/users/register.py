import asyncio
from datetime import datetime

from aiogram import Router
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from DataBase.base import User, sql_safe_insert
from filters.driver_filter import IsDriver
from states.driver_menu import Driver_menu
from states.driver_register import driver_reg

flags = {"throttling_key": "True"}
router = Router()
router.message(IsDriver())
router.message(state=driver_reg)
user = User
@router.message(state=driver_reg.name)
async def name(message: Message, state: FSMContext):
    name = message.text
    await state.update_data(name=name)
    await state.set_state(driver_reg.car_number)
    await message.answer('Теперь напишите номер своего автомобиля в формате "A777AA777"')

@router.message(state=driver_reg.car_number)
async def name(message: Message, state: FSMContext):
    number_car = message.text
    await state.update_data(number_car=number_car)
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="2.5Т"))
    nmarkup.row(types.KeyboardButton(text="5Т"))
    nmarkup.row(types.KeyboardButton(text="10Т"))
    await state.set_state(driver_reg.car_mass)
    await message.answer("Выберите вместимость вашего автомобиля, или укажите приближенный из доступных",
                         reply_markup=nmarkup.as_markup(resize_keyboard=True))

@router.message(state=driver_reg.car_mass)
async def name(message: Message, state: FSMContext):
    if message.text in ['2.5Т', '5Т', '10Т']:
        data = await state.get_data()
        car_mass = message.text
        print(data)
        print(car_mass)
        await sql_safe_insert('users', {'user_id': message.from_user.id, 'username': data['name'].lower(),
                                        'DateTime_come': datetime.now(), 'balance': float(0), 'car_number': data['number_car'].lower(),
                                        'car_mass': car_mass[:-1]})
        nmarkup = ReplyKeyboardBuilder()
        nmarkup.row(types.KeyboardButton(text="Мой кабинет"))
        await state.set_state(Driver_menu.main)
        await message.answer("Ваша регистрация прошла успешно, теперь вы можете получать заказы. \n\n"
                             "Вам будет приходить от меня уведомления о доступном заказе\n"
                             "Вы можете принять заказ и его выполнить или отказаться от него", reply_markup=nmarkup.as_markup(resize_keyboard=True))
    else:
        await message.answer("Формат веса указан неправильно, повторите попытку.")


