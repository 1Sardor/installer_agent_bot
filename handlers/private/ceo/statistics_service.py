from aiogram import Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F

from handlers.api.ceo.statistics import get_statistics
from keyboard.default.ceo_buttons import main_keyboard
from utils.filters import IsCeo

router = Router()
router.message.filter(IsCeo())


@router.message(lambda m: m.text == "📊 Statistika")
async def statistics_menu(message: Message):
    data = await get_statistics()

    total_users = data.get("total_users", 0)
    total_clients = data.get("total_clients", 0)
    overall = data.get("overall_stats", {})
    pending = overall.get("pending", 0)
    in_progress = overall.get("in_progress", 0)
    completed = overall.get("completed", 0)

    # Xodimlar bo'yicha
    user_stats = data.get("user_stats", [])

    text = f"📊 Umumiy Statistikasi:\n\n"
    text += f"👥 Foydalanuvchilar: {total_users}\n"
    text += f"📇 Mijozlar: {total_clients}\n\n"

    text += "📌 Umumiy ishlar:\n"
    text += f"   ⏳ Yangi: {pending:,}\n"
    text += f"   🔄 Bajarilyapti: {in_progress:,}\n"
    text += f"   ✅ Tugatildi: {completed:,}\n\n"

    text += "👤 Xodimlar bo'yicha:\n"
    for user in user_stats:
        text += (
            f"{user['full_name']}\n"
            f"   ✅ Bu oy yakunlangan: {user['this_month_completed']:,}\n"
            f"   🔄 Hozirda faol ishlar: {user['active_in_progress']:,}\n\n"
        )

    await message.answer(text, parse_mode="HTML", reply_markup=main_keyboard())

