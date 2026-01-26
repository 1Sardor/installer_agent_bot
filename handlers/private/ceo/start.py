from aiogram import Router, types, filters
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from handlers.update_role import update_ceo_role
from utils.filters import IsCeo

router = Router()
router.message.filter(IsCeo())


@router.message(filters.CommandStart())
async def start(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    text = """
Assalomu alaykum botga hush kelibsiz!

📌 **Bot Commands**

/help - Show this help message
/update_users - Update CEO role in roles.json (admin only)
/start - Start the bot    
"""
    await message.answer(text)


@router.message(Command("update_users"))
async def update_ceo_command(message: types.Message):
    success = await update_ceo_role()
    if success:
        await message.answer("✅ Users roles updated")
    else:
        await message.answer("❌ Failed to update Users roles")


@router.message(Command("help"))
async def help_command(message: types.Message):
    help_text = """
📌 **Bot Commands**

/help - Show this help message
/update_ceo - Update CEO role in roles.json (admin only)
/start - Start the bot
    """

    await message.answer(help_text)
