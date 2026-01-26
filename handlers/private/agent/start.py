from aiogram import Router, types, filters
from aiogram.fsm.context import FSMContext

from utils.filters import IsAgent

router = Router()
router.message.filter(IsAgent())


@router.message(filters.CommandStart())
async def start(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer('Assalomu alaykum botga hush kelibsiz!')
