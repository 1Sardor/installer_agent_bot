from aiogram import html, types
from aiogram.fsm.context import FSMContext


async def start(message: types.Message, state: FSMContext):
    await message.answer('Assalomu alaykum botga hush kelibsiz!')

