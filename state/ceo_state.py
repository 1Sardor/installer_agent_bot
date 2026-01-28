from aiogram.fsm.state import State, StatesGroup


class AddHodimState(StatesGroup):
    full_name = State()
    chat_id = State()
    status = State()


class EditHodimState(StatesGroup):
    choose_field = State()
    full_name = State()
    chat_id = State()
    status = State()
