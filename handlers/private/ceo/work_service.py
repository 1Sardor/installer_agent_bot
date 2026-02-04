from datetime import datetime, timezone

from aiogram import F
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.api.ceo.works_api import get_works_list, create_work
from keyboard.default.buttons import back_keyboard
from keyboard.default.ceo_buttons import work_keyboard
from keyboard.inline.ceo_buttons import confirm_work_inline_keyboard
from state.ceo_state import WorkState
from utils.filters import IsCeo

router = Router()
router.message.filter(IsCeo())


@router.message(lambda m: m.text == "💼 Ish")
async def show_work_menu(message: Message):
    await message.answer("Ishlar bo'limi:", reply_markup=work_keyboard())


@router.message(F.text == "➕ Yangi Ish")
async def new_work_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("📝 Yangi ish yaratish. \nBirinchi: Ish turini kiriting.", reply_markup=back_keyboard())
    await state.set_state(WorkState.work_type)


@router.message(WorkState.work_type)
async def work_type_handler(message: Message, state: FSMContext):
    await state.update_data(work_type=message.text)
    await message.answer("🏠 Manzilni kiriting:")
    await state.set_state(WorkState.address)


@router.message(WorkState.address)
async def address_handler(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("👤 Mijoz ismi:")
    await state.set_state(WorkState.client_name)


@router.message(WorkState.client_name)
async def client_name_handler(message: Message, state: FSMContext):
    await state.update_data(client_name=message.text)
    await message.answer("📞 Mijoz telefon raqami:")
    await state.set_state(WorkState.client_phone)


@router.message(WorkState.client_phone)
async def client_phone_handler(message: Message, state: FSMContext):
    phone = message.text
    if phone.startswith("+998"):
        phone_number = phone[4:]
    else:
        phone_number = phone

    if not (phone_number.isdigit() and len(phone_number) == 9):
        await message.answer(
            "❌ Telefon raqam noto‘g‘ri. Format: +998991234567 yoki 991234567. Qaytadan kiriting:"
        )
        return

    await state.update_data(client_phone=phone)
    await message.answer("📝 Izoh:")
    await state.set_state(WorkState.izoh)


@router.message(WorkState.izoh)
async def izoh_handler(message: Message, state: FSMContext):
    await state.update_data(izoh=message.text)
    await message.answer("📅 Ish tugash sanasini kiriting (YYYY-MM-DD formatda):")
    await state.set_state(WorkState.finish_date)


@router.message(WorkState.finish_date)
async def finish_date_handler(message: Message, state: FSMContext):
    try:
        finish_date = datetime.strptime(message.text, "%Y-%m-%d").date()
    except ValueError:
        await message.answer("❌ Sana noto‘g‘ri formatda. YYYY-MM-DD formatda kiriting:")
        return
    await state.update_data(finish_date=finish_date)

    data = await state.get_data()
    summary = (
        f"✅ Iltimos ma’lumotlarni tasdiqlang:\n"
        f"Ish turi: <b>{data['work_type']}</b>\n"
        f"Manzil: <b>{data['address']}</b>\n"
        f"Mijoz ismi: <b>{data['client_name']}</b>\n"
        f"Mijoz telefoni: <b>{data['client_phone']}</b>\n"
        f"Izoh: <b>{data['izoh']}</b>\n"
        f"Tugash sanasi: <b>{data['finish_date']}</b>\n\n"
        f"Ha bo‘lsa ✅, Yo‘q bo‘lsa ❌"
    )

    await message.answer(summary, reply_markup=confirm_work_inline_keyboard(), parse_mode="HTML")
    await state.set_state(WorkState.is_correct)


@router.callback_query(F.data == "work_confirm", WorkState.is_correct)
async def work_confirm_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    success = await create_work(data['work_type'], data['address'], data['client_name'], data['client_phone'],
                                data['izoh'], data['finish_date'])
    if not success:
        await callback.message.edit_text("❌ Ish qo'shishda xatolik qayta urunib ko'ring!", reply_markup=work_keyboard())
        return

    await callback.message.edit_text("✅ Yangi ish muvaffaqiyatli qo‘shildi!", reply_markup=work_keyboard())
    await state.clear()


@router.callback_query(F.data == "work_cancel", WorkState.is_correct)
async def work_cancel_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("❌ Jarayon bekor qilindi.")
    await state.clear()


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


@router.message(F.text == "📋 Ishlar ro'yxati")
async def work_list_handler(message: Message):
    works = await get_works_list()

    if not works:
        await message.answer("📭 Hozircha ishlar mavjud emas.")
        return

    text = "📋 <b>Ishlar ro‘yxati</b>\n\n"

    for i, work in enumerate(works, start=1):
        created_by = work.get("created_by_name") or "Biriktirilmagan"
        user_name = work.get("user_name") or "Biriktirilmagan"
        text += (
            f"<b>{i}. {work['work_type']}</b>\n"
            f"📍 Manzil: <b>{work['address']}</b>\n"
            f"👤 Mijoz: <b>{work['client_name']}</b>\n"
            f"📞 Tel: <b>{work['client_phone']}</b>\n"
            f"📝 Izoh: <b>{work['izoh']}</b>\n"
            f"⚡  Ustuvorlik: <b>{get_priority_color(work['finish_date'])}</b>\n"
            f"📌 Holat: <b>{work['status']}</b>\n"
            f"📅 Tugash: <b>{work['finish_date']}</b>\n"
            f"👨‍💼 Yaratgan: <b>{created_by}</b>\n"
            f"👷 Biriktirilgan: <b>{user_name}</b>\n"
            f"──────────────\n"
        )

    await message.answer(text, parse_mode="HTML")
