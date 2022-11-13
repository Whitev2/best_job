import asyncio

from aiogram import Router
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext

from DataBase.base import User
from filters.admin_filter import IsAdmin
from filters.driver_filter import IsDriver
from handlers.users.menu import user_cabinet
from keyboard.admin_kb import main_admin_keyboard
from states.admin_states import Admin_state
from states.driver_register import driver_reg

flags = {"throttling_key": "True"}
router = Router()
router.message(state="*")
user = User()
@router.message(IsAdmin(), commands=['admin'], state="*")
async def admin_menu(message: types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(Admin_state.main_menu)
    await message.answer('Добро пожадовать в админ меню.', reply_markup=main_admin_keyboard())

@router.message(IsDriver(), commands=['start'], flags=flags)
async def client_menu(message: types.Message, state: FSMContext):
    user_info = await user.get_user_info(str(message.from_user.id), 'user_id')
    if not user_info:
        await state.set_state(driver_reg.name)
        await message.answer('Добро пожадовать, пожалуйста, напишите ваше ФИО.')
    else:
        await user_cabinet(message, state)




