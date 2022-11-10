import asyncio
from datetime import datetime

from aiogram import Router, F
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from DataBase.base import Order
from filters.driver_filter import IsDriver
from states.driver_register import driver_reg

flags = {"throttling_key": "True"}
router = Router()
router.message(IsDriver())
router.message(state=driver_reg)
order = Order()

@router.message(F.text == 'Мой кабинет')
async def user_cabinet(message: Message, state: FSMContext):
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="История заказов"))
    nmarkup.row(types.KeyboardButton(text="Мой заработок "))
    await message.answer("Добро пожаловать в личный кабинет кабинет, тут вы можете:\n\n"
                         "— Посмотреть историю последних заказов\n"
                         "— Посмотреть свой заработок за последние 2 недели", reply_markup=nmarkup.as_markup(resize_keyboard=True))

@router.message(F.text == 'История заказов')
async def orders_history(message: Message, state: FSMContext):
    last_orders = await order.get_last_order(user_id=str(message.from_user.id), limit=10)
    print(last_orders)
    text = f"Последние {len(last_orders)} заказов:\n\n"
    for orders in last_orders:
        datestr = orders[1]
        cuont_stop = len(orders[3])
        order_date = datetime.strptime(datestr, "%Y-%m-%d %H:%M:%S.%f")
        text = text + f"Дата заказа: {str(order_date)[:-10]}\nКоличество остановок: {cuont_stop}\n_______________\n"
    await message.answer(text)
@router.message(F.text == 'Мой заработок')
async def user_balance(message: Message, state: FSMContext):
    await message.answer("Ваш заработок за две недели:")
