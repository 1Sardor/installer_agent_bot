from aiogram.fsm.state import State, StatesGroup


class SellerWorkState(StatesGroup):
    work_type = State()
    address = State()
    client_name = State()
    client_phone = State()
    izoh = State()
    finish_date = State()
    is_correct = State()

