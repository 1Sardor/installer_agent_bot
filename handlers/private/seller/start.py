from aiogram import Router, types, filters
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboard.default.seller_keyboard import main_keyboard
from utils.filters import IsSeller

router = Router()
router.message.filter(IsSeller())


@router.message(filters.CommandStart())
async def start(message: Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer('Assalomu alaykum Seller botga hush kelibsiz!', reply_markup=main_keyboard())


@router.message(lambda m: m.text == "⬅️ Orqaga")
async def back_to_main(message: types.Message, state: FSMContext):
    await state.clear()
    await message.answer("Asosiy menyu:", reply_markup=main_keyboard())

