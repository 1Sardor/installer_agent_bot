from aiogram.fsm.state import State, StatesGroup


class AgentWorkState(StatesGroup):
    work_type = State()
    address = State()
    client_name = State()
    client_phone = State()
    izoh = State()
    finish_date = State()
    is_correct = State()


class AcceptWorkState(StatesGroup):
    work = State()


class CompleteWorkState(StatesGroup):
    chat_id = State()
    work = State()
    document = State()
    image = State()
    explain = State()
