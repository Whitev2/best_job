from aiogram.fsm.state import StatesGroup, State


class Admin_state(StatesGroup):
    main_menu = State()
    confirm_text = State()
    driver_edit = State()