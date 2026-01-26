from aiogram import html, types
from aiogram.fsm.context import FSMContext

from aiogram_bot_template import states


async def start(message: types.Message, state: FSMContext) -> None:
    await message.answer('Assalomu alaykum botga hush kelibsiz!')