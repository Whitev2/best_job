import asyncio

from aiogram import Router, F
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from filters.driver_filter import IsDriver
from states.driver_register import driver_reg

flags = {"throttling_key": "True"}
router = Router()
router.message(IsDriver())
router.message(state=driver_reg)


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
    await message.answer("Все ваши заказы за две недели:")
@router.message(F.text == 'Мой заработок')
async def user_balance(message: Message, state: FSMContext):
    await message.answer("Ваш заработок за две недели:")
