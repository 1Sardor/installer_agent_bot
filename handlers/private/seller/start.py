from aiogram import Router, types, filters
from aiogram.fsm.context import FSMContext

from utils.filters import IsSeller

router = Router()
router.message.filter(IsSeller())


@router.message(filters.CommandStart())
async def start(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer('Assalomu alaykum botga hush kelibsiz!')
