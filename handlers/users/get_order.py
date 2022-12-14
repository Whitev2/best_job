import asyncio
import json
from datetime import datetime

from aiogram import Router, F
from aiogram import types
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, order_info
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

from DataBase.base import list_read, redis_just_one_write, \
    data_getter, del_key, Order, User, sql_safe_insert
from filters.driver_filter import IsDriver
from handlers.users.menu import user_cabinet
from loader import all_data
from payments.payroll import salary
from points import one_point
from states.driver_register import driver_reg
from states.orders_states import Order_driver

flags = {"throttling_key": "True"}
router = Router()
router.message(IsDriver())
data = all_data()
bot = data.get_bot()

order = Order()
user = User()

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
    await state.set_state(Order_driver.driver_here)
    await state.update_data(count=0)
    await query.message.delete()
    await redis_just_one_write(f"User: Status_delivery: {query.from_user.id}", "1")
    user_id = query.from_user.id
    order_info = await list_read(f"Orders: {user_id}: ")
    count_rows = await order.get_last_order(f"{query.from_user.id}")
    if len(count_rows) != 0:
        count_rows = count_rows[0][0]
    else:
        count_rows = 0
    jsonorder = json.dumps(order_info)

    await sql_safe_insert('orders', {"id": count_rows + 1, "Executor_id": str(query.from_user.id),
                                     "DateTime_order": datetime.utcnow(), "extradition": jsonorder, "status": False,
                                     "order_time": None, 'price': 0.0})
    await del_key(f"Orders: {user_id}: ")
    nmarkup = ReplyKeyboardBuilder()
    nmarkup.row(types.KeyboardButton(text="Я приехал"))
    await query.message.answer(f'Вы подтвердили заказ, нажмите <b>Я приехал</b> по приезде.'
                               f' \n\nВаша первая точка: {one_point}',
                               reply_markup=nmarkup.as_markup(resize_keyboard=True))

@router.callback_query(lambda call: 'driver_cancel_order' in call.data)
async def driver_cancel_order(query: types.CallbackQuery, state: FSMContext):
    await query.message.answer('Вы отказылись от заказа')


@router.message(F.text == 'Я приехал', StateFilter(Order_driver.driver_here))
async def driver_here(message: Message, state: FSMContext):
    data = await state.get_data()
    count = data.get("count")

    driver_order = await order.get_last_order(str(message.from_user.id))
    time_start = driver_order[0][1]
    time_start = datetime.strptime(time_start, "%Y-%m-%d %H:%M:%S.%f")
    if len(driver_order[0][3]) > count:
        address = driver_order[0][3][count].split('//')
        await message.answer(f"Отлично! \n\nВаш следующий адрес: {address[0]}\n"
                             f"Артикуль: {address[1]}\n"
                             f"Число коробок: {address[2]}")
        await state.update_data(count=count + 1)
    else:
        user_balance = await user.get_balance(message.from_user.id)
        await redis_just_one_write(f"User: Status_delivery: {message.from_user.id}", "0")
        order_price = await salary(message.from_user.id, len(driver_order[0][3]))
        print(user_balance)
        print(order_price)
        new_user_balance = float(user_balance) + float(order_price)
        date_end = datetime.now() - time_start
        bata = all_data()
        user_info = await user.get_user({'user_id': message.from_user.id})
        try:
            await bot.send_message(chat_id=bata.info_channel, text=f"Водитель: {user_info[0][1].upper()}\n"
                                                               f"Номер авто: {user_info[0][3].upper()}\n\n"
                                                                   f"<b>Завершил заказ: ID-{driver_order[0][0]}</b>\n"
                                                                   )
        except Exception:
            pass
        print(new_user_balance)
        await user.sql_update('users', {'balance': new_user_balance}, {'user_id': message.from_user.id})
        await order.sql_update_orders('orders', str(message.from_user.id), {'order_time': f'{date_end}'})
        await order.sql_update_orders('orders', str(message.from_user.id), {'price': f'{order_price}'})
        await message.answer("Маршрут завершен, оплату за заказ вы можете посмотреть в своём кабинете.")
        await state.set_state(driver_reg.main)
        await user_cabinet(message, state)

