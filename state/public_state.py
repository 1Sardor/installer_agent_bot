from aiogram.fsm.state import StatesGroup, State


class RegisterState(StatesGroup):
    waiting_phone = State()


class RatingState(StatesGroup):
    waiting_standard = State()
    waiting_satisfaction = State()
