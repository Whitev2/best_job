from aiogram.dispatcher.filters.state import StatesGroup, State


class driver_reg(StatesGroup):
    name = State()
    car_number = State()
    car_mass = State()