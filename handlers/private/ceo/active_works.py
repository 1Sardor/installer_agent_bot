from datetime import datetime, timezone

from aiogram import F
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.api.ceo.works_api import get_active_works
from keyboard.default.ceo_buttons import main_keyboard
from utils.filters import IsCeo

router = Router()
router.message.filter(IsCeo())


def get_priority_color(finish_date):
    if not finish_date:
        return "⚡ Noma'lum"

    if isinstance(finish_date, str):
        try:
            finish_date = datetime.fromisoformat(finish_date)
        except Exception:
            return "⚡ Noma'lum"

    if finish_date.tzinfo is None:
        finish_date = finish_date.replace(tzinfo=timezone.utc)

    now = datetime.now(timezone.utc)
    days_left = (finish_date - now).days

    if days_left >= 5:
        return "🟩 Yashil"
    elif 2 <= days_left <= 4:
        return "🟨 Sariq"
    elif 0 <= days_left <= 1:
        return "🟥 Qizil"
    else:
        return "❌ Kechikdi"


@router.message(F.text == "⚡ Faol Ishlar")
async def send_active_works(message: Message):
    works = await get_active_works()

    if not works:
        await message.answer("✅ Hozirda faol ishlar mavjud emas.")
        return

    text = "🔄 Hozirda faol ishlar:\n\n"

    for w in works:
        text += (
            f"🛠 {w['work_type']}\n"
            f"   🆔 ID: <b>{w['id']}</b>\n"
            f"   👤 Bajaruvchi: <b>{w.get('user_name', '-')}</b>\n"
            f"   ✍  Yaratuvchi: <b>{w.get('created_by_name', '-')}</b>\n"
            f"   🏠 Manzil: <b>{w['address']}</b>\n"
            f"   📞 Mijoz: <b>{w['client_name']} ({w['client_phone']})</b>\n"
            f"   ⏳ Yakunlanishi: <b>{w['finish_date']}</b>\n"
            f"   ⚡  Priority: <b>{get_priority_color(w['finish_date'])}</b>\n"
            f"   📋 Status: <b>{w['status']}</b>\n"
            f"   🕒 Yaratilgan: <b>{w['created_at']}</b>\n\n"
        )

    await message.answer(text, main_keyboard=main_keyboard(), parse_mode="HTML")
