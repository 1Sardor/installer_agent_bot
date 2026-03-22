from datetime import datetime, timezone

from aiogram import F
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.api.ceo.works_api import create_work, get_works_list, get_active_works, get_will_be_free, get_works_types_list
from keyboard.default.buttons import back_keyboard
from keyboard.default.seller_keyboard import work_keyboard, main_keyboard
from keyboard.inline.ceo_buttons import confirm_work_inline_keyboard
from keyboard.default.ceo_buttons import generate_work_type_buttons
from utils.filters import IsSeller
from state.seller_state import SellerWorkState

router = Router()
router.message.filter(IsSeller())


@router.message(lambda m: m.text == "💼 Ish")
async def show_work_menu(message: Message):
    await message.answer("Ishlar bo'limi:", reply_markup=work_keyboard())


@router.message(F.text == "➕ Yangi Ish")
async def new_work_start(message: Message, state: FSMContext):
    await state.clear()
    data = await get_will_be_free()
    await message.answer(f"Note: Agentlar taxminan {data.get('data')} kundan keyin ishlarini tugatadi.\nBirinchi: Ish turini kiriting.", reply_markup=await generate_work_type_buttons())
    await state.set_state(SellerWorkState.work_type)


@router.message(SellerWorkState.work_type)
async def work_type_handler(message: Message, state: FSMContext):

    work_types = await get_works_types_list()
    if message.text not in [i["name"] for i in work_types]:
        await message.answer("Ish turini Tanlang.", reply_markup=await generate_work_type_buttons())
        await state.set_state(SellerWorkState.work_type)
        return

    await state.update_data(work_type=message.text)
    await state.update_data(chat_id=message.chat.id)
    await message.answer("🏠 Manzilni kiriting:", reply_markup=back_keyboard())
    await state.set_state(SellerWorkState.address)


@router.message(SellerWorkState.address)
async def address_handler(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("👤 Mijoz ismi:")
    await state.set_state(SellerWorkState.client_name)


@router.message(SellerWorkState.client_name)
async def client_name_handler(message: Message, state: FSMContext):
    await state.update_data(client_name=message.text)
    await message.answer("📞 Mijoz telefon raqami: \nNa'muna: 991234567")
    await state.set_state(SellerWorkState.client_phone)


@router.message(SellerWorkState.client_phone)
async def client_phone_handler(message: Message, state: FSMContext):
    phone = message.text.replace(" ", "").replace("+", "")
    if not phone.isdigit() or len(phone) != 9:
        await message.answer(
            "❌ Telefon raqam noto‘g‘ri. Format: 991234567. Qaytadan kiriting:"
        )
        return

    await state.update_data(client_phone=phone)
    await message.answer("📝 Izoh:")
    await state.set_state(SellerWorkState.izoh)


@router.message(SellerWorkState.izoh)
async def izoh_handler(message: Message, state: FSMContext):
    await state.update_data(izoh=message.text)
    await message.answer("📅 Ish bajarilish vaqtini kunda kiriting misol uchun (1 yoki 2):")
    await state.set_state(SellerWorkState.deadline)


@router.message(SellerWorkState.deadline)
async def izoh_handler(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Iltimos, faqat raqam kiriting (1 yoki 2):")
        await state.set_state(SellerWorkState.deadline)
        return
        
    await state.update_data(deadline=message.text)
    await message.answer("📅 Ish tugash sanasini kiriting (YYYY-MM-DD formatda):")
    await state.set_state(SellerWorkState.finish_date)


@router.message(SellerWorkState.finish_date)
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
    await state.set_state(SellerWorkState.is_correct)


@router.callback_query(F.data == "work_confirm", SellerWorkState.is_correct)
async def work_confirm_handler(callback: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    
    success = await create_work(data['chat_id'], data['work_type'], data['address'], data['client_name'], data['client_phone'],
                                data['izoh'], data['deadline'], data['finish_date'])
    
    if not success:
        await callback.message.answer("❌ Ish qo'shishda xatolik qayta urunib ko'ring!", reply_markup=work_keyboard())
        await callback.message.delete()

        return

    await callback.message.answer("✅ Yangi ish muvaffaqiyatli qo‘shildi!", reply_markup=work_keyboard())
    await callback.message.delete()
    await state.clear()


@router.callback_query(F.data == "work_cancel", SellerWorkState.is_correct)
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

    for i, work in enumerate(works, start=1):
        created_by = work.get("created_by_name") or "Biriktirilmagan"
        user_name = work.get("user_name") or "Biriktirilmagan"
        text = (
            f"<b>{i}. {work['work_type']}</b>\n"
            f"📍 Manzil: <b>{work['address']}</b>\n"
            f"👤 Mijoz: <b>{work['client_name']}</b>\n"
            f"📞 Tel: <b>{work['client_phone']}</b>\n"
            f"📝 Izoh: <b>{work['izoh']}</b>\n"
            f"⚡  Ustuvorlik: <b>{get_priority_color(work['finish_date'])}</b>\n"
            f"📌 Holat: <b>{work['status']}</b>\n"
            f"📅 Tugash: <b>{work['finish_date']}</b>\n"
            f"📅 Deadline: <b>{work['deadline']} kun</b>\n"
            f"👨‍💼 Yaratgan: <b>{created_by}</b>\n"
            f"👷 Biriktirilgan: <b>{user_name}</b>\n"
        )
        document_url = work.get("document")
        if document_url:
            await message.answer_document(
                document=document_url,
                caption=text,
                parse_mode="HTML"
            )
        else:
            await message.answer(
                text,
                parse_mode="HTML"
            )


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
            f"   👤 Bajaruvchi: <b>{w.get('user_name', '-')}</b>\n"
            f"   ✍  Yaratuvchi: <b>{w.get('created_by_name', '-')}</b>\n"
            f"   🏠 Manzil: <b>{w['address']}</b>\n"
            f"   📞 Mijoz: <b>{w['client_name']} ({w['client_phone']})</b>\n"
            f"   ⏳ Yakunlanishi: <b>{w['finish_date']}</b>\n"
            f"   ⚡  Priority: <b>{get_priority_color(w['finish_date'])}</b>\n"
            f"   📋 Status: <b>{w['status']}</b>\n"
            f"   🕒 Yaratilgan: <b>{w['created_at']}</b>\n\n"
        )

    await message.answer(text, reply_markup=main_keyboard(), parse_mode="HTML")
