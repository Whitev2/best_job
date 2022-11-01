import asyncio

from aiogram import Router
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext

from states.admin_states import Admin_state

flags = {"throttling_key": "True"}
router = Router(Admin_state.main_menu)

@router.message(commands=['menu'], flags=flags)
async def commands_start_menu(message: types.Message, state: FSMContext):

     await message.answer('Эта команда будет доступна только после первого прохождения бота')