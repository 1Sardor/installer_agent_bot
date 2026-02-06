from aiogram import Router, types, filters
from aiogram.fsm.context import FSMContext

from keyboard.default.agent_button import main_keyboard
from utils.filters import IsAgent

router = Router()
router.message.filter(IsAgent())


@router.message(filters.CommandStart())
async def start(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer('Assalomu alaykum Agent botga hush kelibsiz!', reply_markup=main_keyboard())


@router.message(lambda m: m.text == "⬅️ Orqaga")
async def back_to_main(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Asosiy menyu:", reply_markup=main_keyboard())

