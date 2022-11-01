import asyncio

from aiogram import Router
from aiogram import types
from aiogram.dispatcher.fsm.context import FSMContext

from filters.driver_filter import IsDriver

flags = {"throttling_key": "True"}
router = Router()
router.message(IsDriver())

