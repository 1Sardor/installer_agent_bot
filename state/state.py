from aiogram.fsm.state import State, StatesGroup


class RegisterState(StatesGroup):
    chat_id = State()
    phone = State()
    