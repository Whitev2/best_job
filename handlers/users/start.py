import asyncio

from aiogram import Router
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext

from filters.admin_filter import IsAdmin
from filters.driver_filter import IsDriver
from keyboard.admin_kb import main_admin_keyboard
from states.admin_states import Admin_state

flags = {"throttling_key": "True"}
router = Router()
router.message(IsDriver())

@router.message(IsDriver(), commands=['start'], flags=flags)
async def admin_menu(message: types.Message, state: FSMContext):
    await message.answer('Добро пожадовать, пожалуйста, напишите номер своего автомобиля.')


@router.message(IsAdmin(), commands=['admin'], flags=flags)
async def admin_menu(message: types.Message, state: FSMContext):
    await state.set_state(Admin_state.main_menu)
    await message.answer('Добро пожадовать в админ меню.', reply_markup=main_admin_keyboard())

