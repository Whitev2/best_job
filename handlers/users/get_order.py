import asyncio

from aiogram import Router, F
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message, order_info
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from DataBase.base import list_read, redis_just_one_write
from filters.driver_filter import IsDriver
from loader import all_data
from states.driver_register import driver_reg

flags = {"throttling_key": "True"}
router = Router()
router.message(IsDriver())
data = all_data()
bot = data.get_bot()


async def send_order(user_id, text):
    try:
        nmarkup = InlineKeyboardBuilder()
        nmarkup.button(text='Принять', callback_data=f'driver_confirm_order')
        nmarkup.button(text='Отказаться', callback_data=f'driver_cancel_order')
        await bot.send_message(chat_id=user_id, text=text, reply_markup=nmarkup.as_markup(resize_keyboard=True))
        return True
    except Exception:
        return False

@router.callback_query(lambda call: 'driver_confirm_order' in call.data)
async def driver_confirm_order(query: types.CallbackQuery, state: FSMContext):
    await redis_just_one_write("User: Status_delivery:", "1")
    user_id = query.from_user.id
    order_info = await list_read(f"Orders: {user_id}: ")
    print(order_info)
    await query.message.answer('Вы подтвердили заказ')

@router.callback_query(lambda call: 'driver_cancel_order' in call.data)
async def driver_cancel_order(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer('Вы отказылись от заказа')

