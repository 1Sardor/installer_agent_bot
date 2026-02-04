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


class AddClientState(StatesGroup):
    full_name = State()
    phone = State()
    address = State()


class AddRazxodState(StatesGroup):
    miqdor = State()
    izoh = State()
    image = State()
    is_correct = State()


class WorkState(StatesGroup):
    work_type = State()
    address = State()
    client_name = State()
    client_phone = State()
    izoh = State()
    finish_date = State()
    is_correct = State()

