from aiogram.dispatcher.filters.state import StatesGroup, State


class driver_reg(StatesGroup):
    main = State()
    name = State()
    car_number = State()
    car_number_edit = State()
    car_mass = State()