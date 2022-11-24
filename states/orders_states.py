from aiogram.fsm.state import StatesGroup, State


class Order_state(StatesGroup):
    main = State()
    add_stop = State()
    address = State()
    send_order = State

class Order_driver(StatesGroup):
    driver_here = State()
