from aiogram.fsm.state import StatesGroup, State


class RegisterState(StatesGroup):
    waiting_phone = State()
