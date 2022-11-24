import asyncio
from datetime import datetime

from aiogram import Router, F
from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from DataBase.base import Order, User
from filters.driver_filter import IsDriver
from states.driver_register import driver_reg

flags = {"throttling_key": "True"}
router = Router()
router.message(IsDriver())
router.message(StateFilter(driver_reg))
order = Order()
user = User()

@router.message(F.text == 'Мой кабинет')
async def user_cabinet(message: Message, state: FSMContext):
    await state.clear()
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="История заказов"))
    nmarkup.row(types.KeyboardButton(text="Мой заработок "))
    nmarkup.row(types.KeyboardButton(text="Изменить номер авто"))
    await message.answer("Добро пожаловать в личный кабинет кабинет, тут вы можете:\n\n"
                         "— Посмотреть историю последних заказов\n"
                         "— Посмотреть свой заработок за последние 2 недели", reply_markup=nmarkup.as_markup(resize_keyboard=True))

@router.message(F.text == 'Отменить')
async def back(message: Message, state: FSMContext):
    await user_cabinet(message, state)

@router.message(F.text == 'Изменить номер авто')
async def change_car_num(message: Message, state: FSMContext):
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="Отменить"))
    await state.set_state(driver_reg.car_number_edit)
    await message.answer('напишите номер своего автомобиля в формате "A777AA777"',
                         reply_markup=nmarkup.as_markup(resize_keyboard=True))

@router.message(StateFilter(driver_reg.car_number_edit))
async def name(message: Message, state: FSMContext):
    number_car = message.text
    await user.sql_update('users', {'car_number': message.text.lower()}, {'user_id': message.from_user.id})
    await message.answer("Ваш номер авто был изменён")
    await user_cabinet(message, state)


@router.message(F.text == 'История заказов')
async def orders_history(message: Message, state: FSMContext):
    last_orders = await order.get_last_order(user_id=str(message.from_user.id), limit=10)
    text = f"Последние {len(last_orders)} заказов:\n\n"
    for orders in last_orders:
        datestr = orders[1]
        cuont_stop = len(orders[3])
        order_date = datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S.%f")
        text = text + f"Дата заказа: {str(order_date)[:-10]}\nКоличество остановок: {cuont_stop}\n_______________\n"
    await message.answer(text)
@router.message(F.text == 'Мой заработок')
async def user_balance(message: Message, state: FSMContext):
    last_order = await order.get_last_order(user_id=str(message.from_user.id))
    user_balance = await user.get_balance(message.from_user.id)
    try:
        order_price = last_order[0][6]
    except:
        order_price = 0

    await message.answer(f"За последний заказ вам начислено: {float(order_price)}р.\n"
                         f"Ваш баланс до расчетного периода: {user_balance}р.")
