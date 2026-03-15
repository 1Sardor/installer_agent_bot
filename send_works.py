from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime
import asyncio
from handlers.api.agent.work_api import get_active_work_for_agent
from config import bot
import json
from pytz import timezone

scheduler = AsyncIOScheduler()


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


async def get_active_works_text():
    works = await get_active_work_for_agent()

    if not works:
        return "✅ Hozirda faol ishlar mavjud emas."


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

    return text


async def send_daily_message():
    text = await get_active_works_text()

    with open("data.json", "r") as f:
        data = json.load(f)

    ids = list(data.keys())
    for i in ids:
        await bot.send_message(chat_id=i, text=text)


def start_scheduler():
    scheduler.add_job(
        send_daily_message,
        "cron",
        hour=13,
        minute=50
    )
    scheduler.start()
