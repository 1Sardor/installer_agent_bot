from aiogram import Router, types, filters
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command

from handlers.api.ceo.update_role import update_ceo_role
from utils.filters import IsCeo
from keyboard.default.ceo_buttons import main_keyboard
from keyboard.default.buttons import back_keyboard

router = Router()
router.message.filter(IsCeo())


@router.message(filters.CommandStart())
async def start(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    text = """
📌 Bot buyruqlari

/help – Yordam xabarini ko‘rsatish
/update_users – Foydalanuvchilarni yangilash
/start – Botni ishga tushirish
"""
    await message.answer(text, reply_markup=main_keyboard())


@router.message(Command("update_users"))
async def update_ceo_command(message: types.Message):
    success = await update_ceo_role()
    print(success)
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
