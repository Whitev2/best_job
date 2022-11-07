import asyncio
import os
from datetime import datetime

from aiogram import Router, F, Bot
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.exceptions import TelegramBadRequest
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from DataBase.base import sql_safe_insert, sql_safe_select, data_getter, redis_just_one_write, list_write, \
    redis_just_one_read
from filters.admin_filter import IsAdmin
from handlers.users.get_order import send_order
from handlers.users.start import admin_menu
from loader import all_data
from states.admin_states import Admin_state
from states.orders_states import Order_state

router = Router()
router.message(state=(Admin_state, Order_state))
data = all_data()
bot = data.get_bot()

@router.message(F.text == 'Заказы')
async def orders(message: Message, state: FSMContext):
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="Малая (2.5 ТОННЫ)"))
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
    msg_id_list = list()
    if len(request) > 0:
        for driver in request:
            nmarkup = InlineKeyboardBuilder()
            nmarkup.button(text='Создать заказ', callback_data=f'{driver[0]}|new_order')
            mesg = await message.answer(f'Водитель: {driver[1]}\nНомер автомобиля: {driver[-2]}', reply_markup=nmarkup.as_markup())
            await list_write("Admin: drever_message_id_list:", mesg.message_id)
    else:
        await message.answer('Увы, водителей нет')



@router.callback_query(lambda call: 'new_order' in call.data)
async def new_order(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    data = query.data.split('|')  # user_id|tag
    nmarkup = InlineKeyboardBuilder()
    nmarkup.button(text='Добавить остановку', callback_data=f'add_stop')
    nmarkup.button(text='Отменить', callback_data=f'order_delete')
    text = 'Ваш заказ на доставку:\n\n' \
           'Точка 1: Первый адрес\n'
    text_2 = '!!Добавляйте точки остановок и это сообщение будет дополняться'
    bot_message = await query.message.answer(text+text_2, reply_markup=nmarkup.as_markup())
    message_id = bot_message.message_id
    await state.update_data(message_id=message_id)
    await state.update_data(user_id=data[0])
    await state.update_data(text=text)
    await state.update_data(count=1)
    await state.set_state(Order_state.add_stop)


@router.callback_query(lambda call: 'add_stop' in call.data, state=Order_state.add_stop)
async def add_stop(query: types.CallbackQuery, state: FSMContext):
    await state.set_state(Order_state.address)
    data = await state.get_data()
    last_count = data.get('count')
    await state.update_data(count=int(last_count) + 1)
    router_message = await query.message.answer("Пожалуйста, введите адрес точки разгрузки")
    await state.update_data(router_message_id=router_message.message_id)


@router.message(state=Order_state.address)
async def address(message: types.Message, state: FSMContext):
    await message.delete()
    data = await state.get_data()
    last_count = data.get('count')
    message_id = data.get('message_id')
    user_id = data.get('user_id')
    router_message_id = data.get('router_message_id')
    await bot.delete_message(chat_id=user_id, message_id=router_message_id)

    address = message.text
    nmarkup = InlineKeyboardBuilder()
    nmarkup.button(text='Добавить остановку', callback_data=f'add_stop')
    nmarkup.button(text='Создать заказ', callback_data=f'{user_id}|confirm_order')

    text = data.get("text")
    text = text + "\n\n__________________\n" + f"Точка: {last_count}\n" + f"Адрес: {address}"

    await state.update_data(user_id=user_id)
    await state.update_data(text=text)

    await bot.edit_message_text(text=text, chat_id=user_id, message_id=message_id, reply_markup=nmarkup.as_markup())
    await list_write(f"{user_id}: Orders: ", address)
    await state.set_state(Order_state.add_stop)


@router.callback_query(lambda call: 'confirm_order' in call.data, state=Order_state.add_stop)
async def add_stop(query: types.CallbackQuery, state: FSMContext):
    await query.message.delete()
    query_data = query.data.split('|')
    state_data = await state.get_data()
    user_id = query_data[0]
    text = state_data.get('text')

    if await send_order(user_id=user_id, text=text):
        await query.message.answer("Заказ отправлен водителю, ожидает подтверждения")
    else:
        await query.message.answer("Водитель не получил заказ, возможно он заблокировал бота")
    await state.set_state(Admin_state.main_menu)






