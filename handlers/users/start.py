import asyncio

from aiogram import Router
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext

from filters.driver_filter import IsDriver

flags = {"throttling_key": "True"}
router = Router()
router.message(IsDriver())

@router.message(IsDriver(), commands=['start'], flags=flags)
async def admin_menu(message: types.Message, state: FSMContext):
    await message.answer('Добро пожадовать, пожалуйста, напишите номер своего автомобиля.')
@router.message(commands=['admin'], flags=flags)
async def admin_menu(message: types.Message, state: FSMContext):
    await message.answer('Добро пожадовать в админ меню.')

