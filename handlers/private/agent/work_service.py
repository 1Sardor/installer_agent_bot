from datetime import datetime, timezone

from aiogram import F
from aiogram import Router, types
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from handlers.api.agent.work_api import get_installed_works_list, get_active_work_for_agent, accept_work, complete_work
from handlers.api.ceo.works_api import create_work
from handlers.views import download_image
from keyboard.default.buttons import back_keyboard
from keyboard.default.agent_button import work_keyboard, main_keyboard
from keyboard.inline.agent_buttons import accept_work_inline_keyboard, complete_work_inline_keyboard, ha_yoq_keyboard
from keyboard.inline.ceo_buttons import confirm_work_inline_keyboard
from utils.filters import IsAgent
from state.agent_state import AgentWorkState, AcceptWorkState, CompleteWorkState

router = Router()
router.message.filter(IsAgent())


@router.message(lambda m: m.text == "💼 Ish")
async def show_work_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Ishlar bo'limi:", reply_markup=work_keyboard())


@router.message(F.text == "➕ Yangi Ish")
async def new_work_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("📝 Yangi ish yaratish. \nBirinchi: Ish turini kiriting.", reply_markup=back_keyboard())
    await state.set_state(AgentWorkState.work_type)


@router.message(AgentWorkState.work_type)
async def work_type_handler(message: Message, state: FSMContext):
    await state.update_data(work_type=message.text)
    await state.update_data(chat_id=message.chat.id)
    await message.answer("🏠 Manzilni kiriting:")
    await state.set_state(AgentWorkState.address)


@router.message(AgentWorkState.address)
async def address_handler(message: Message, state: FSMContext):
    await state.update_data(address=message.text)
    await message.answer("👤 Mijoz ismi:")
    await state.set_state(AgentWorkState.client_name)


@router.message(AgentWorkState.client_name)
async def client_name_handler(message: Message, state: FSMContext):
    await state.update_data(client_name=message.text)
    await message.answer("📞 Mijoz telefon raqami:")
    await state.set_state(AgentWorkState.client_phone)


@router.message(AgentWorkState.client_phone)
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
    await state.set_state(AgentWorkState.izoh)


@router.message(AgentWorkState.izoh)
async def izoh_handler(message: Message, state: FSMContext):
    await state.update_data(izoh=message.text)
    await message.answer("📅 Ish tugash sanasini kiriting (YYYY-MM-DD formatda):")
    await state.set_state(AgentWorkState.finish_date)


@router.message(AgentWorkState.finish_date)
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
    await state.set_state(AgentWorkState.is_correct)


@router.callback_query(F.data == "work_confirm", AgentWorkState.is_correct)
async def work_confirm_handler(callback: CallbackQuery, state: FSMContext):
    print("workeeeed")
    data = await state.get_data()

    success = await create_work(data['chat_id'], data['work_type'], data['address'], data['client_name'], data['client_phone'],
                                data['izoh'], data['finish_date'])
    if not success:
        await callback.message.answer("❌ Ish qo'shishda xatolik qayta urunib ko'ring!", reply_markup=work_keyboard())
        await callback.message.delete()

        return

    await callback.message.answer("✅ Yangi ish muvaffaqiyatli qo‘shildi!", reply_markup=work_keyboard())
    await callback.message.delete()
    await state.clear()


@router.callback_query(F.data == "work_cancel", AgentWorkState.is_correct)
async def work_cancel_handler(callback: CallbackQuery, state: FSMContext):
    await callback.message.edit_text("❌ Jarayon bekor qilindi.", reply_markup=work_keyboard())
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


@router.message(F.text == "📋 O'rnatilgan ishlar ro'yxati")
async def work_list_handler(message: Message):
    chat_id = message.chat.id
    works = await get_installed_works_list(chat_id, 3)

    if not works:
        await message.answer("📭 Hozircha siz o'rnatgan ishlar mavjud emas.")
        return

    text = "📋 <b>Ishlar ro‘yxati</b>\n\n"

    for i, work in enumerate(works, start=1):
        created_by = work.get("created_by_name") or "Biriktirilmagan"
        user_name = work.get("user_name") or "Biriktirilmagan"
        text += (
            f"<b>{i}. {work['work_type']}</b>\n"
            f"🆔 ID: <b>{work['id']}</b>\n"
            f"📍 Manzil: <b>{work['address']}</b>\n"
            f"👤 Mijoz: <b>{work['client_name']}</b>\n"
            f"📞 Tel: <b>{work['client_phone']}</b>\n"
            f"📝 Izoh: <b>{work['izoh']}</b>\n"
            f"📌 Holat: <b>{work['status']}</b>\n"
            f"📅 Tugash: <b>{work['finish_date']}</b>\n"
            f"📅 Qabul qilingan: <b>{work['accepted_at']}</b>\n"
            f"📅 Bajarilgan sana: <b>{work['completed_at']}</b>\n"
            f"👨‍💼 Yaratgan: <b>{created_by}</b>\n"
            f"👷 Biriktirilgan: <b>{user_name}</b>\n"
            f"──────────────\n"
        )

    await message.answer(text, parse_mode="HTML")


@router.message(F.text == "⚡ Faol Ishlar")
async def send_active_works(message: Message, state: FSMContext):
    await state.clear()
    works = await get_active_work_for_agent()
    await state.set_state(AcceptWorkState.work)
    if not works:
        await message.answer("✅ Hozirda faol ishlar mavjud emas.")
        return

    for count, w in enumerate(works, start=1):
        text = (
            f"🔢 №: <b>{count}</b>\n"
            f"🆔 ID: <b>{w['id']}</b>\n"
            f"✍  Yaratuvchi: <b>{w.get('created_by_name', '-')}</b>\n"
            f"🏠 Manzil: <b>{w['address']}</b>\n"
            f"👤 Mijoz ismi: <b>{w['client_name']}</b>\n"
            f"📞 Telefon raqami: <b>{w['client_phone']}</b>\n"
            f"⏳ Yakunlanishi: <b>{w['finish_date']}</b>\n"
            f"⚡  Priority: <b>{get_priority_color(w['finish_date'])}</b>\n"
            f"📋 Status: <b>{w['status']}</b>\n"
            f"🕒 Yaratilgan: <b>{w['created_at']}</b>\n\n"
        )
        await message.answer(text, reply_markup=accept_work_inline_keyboard(w['id']), parse_mode="HTML")


@router.callback_query(F.data.startswith("accept_work:"), AcceptWorkState.work)
async def accept_work_handler(callback: types.CallbackQuery):
    work_id = callback.data.split(":")[1]
    chat_id = callback.message.chat.id
    success = await accept_work(chat_id, work_id)
    if not success:
        await callback.message.answer("❌ Bu ish boshqa agent tomonidan qabul qilingan!")
        await callback.message.delete()
        return

    await callback.answer("✅ Ish qabul qilindi", show_alert=False)

    await callback.message.edit_text(
        f"✅ Ish qabul qilindi!\n🆔 Ish ID: {work_id}"
    )

@router.message(F.text == "🛠 Mening ishlarim")
async def send_active_works(message: Message, state: FSMContext):
    await state.clear()
    chat_id = message.chat.id
    works = await get_installed_works_list(chat_id, 2)

    if not works:
        await message.answer("✅ Hozirda siz qabul qilgan ishlar mavjud emas.")
        return

    for w in works:
        text = (
            f"🛠 {w['work_type']}\n"
            f"   🆔 ID: <b>{w['id']}</b>\n"
            f"   👤 Bajaruvchi: <b>{w.get('user_name', '-')}</b>\n"
            f"   ✍  Yaratuvchi: <b>{w.get('created_by_name', '-')}</b>\n"
            f"   🏠 Manzil: <b>{w['address']}</b>\n"
            f"   📞 Mijoz: <b>{w['client_name']} ({w['client_phone']})</b>\n"
            f"   ⏳ Yakunlanishi: <b>{w['finish_date']}</b>\n"
            f"   ⚡  Priority: <b>{get_priority_color(w['finish_date'])}</b>\n"
            f"   📋 Status: <b>{w['status']}</b>\n"
            f"   🕒 Yaratilgan: <b>{w['created_at']}</b>\n"
            f"   🕒 Qabul qilingan vaqt: <b>{w['accepted_at']}</b>\n\n"
        )

        await message.answer(text, reply_markup=complete_work_inline_keyboard(w['id']), parse_mode="HTML")


@router.callback_query(F.data.startswith("complete_work:"))
async def complete_work_start(callback: types.CallbackQuery, state: FSMContext):
    work_id = callback.data.split(":")[1]

    await state.clear()
    await state.set_state(CompleteWorkState.document)
    await state.update_data(work_id=work_id)
    await state.update_data(chat_id=callback.message.chat.id)

    await callback.answer("✅ Ish tanlandi")

    await callback.message.answer(
        f"🆔 Ish ID: {work_id}\n\n📄 Iltimos, hujjatni yuboring", reply_markup=back_keyboard()
    )


@router.message(CompleteWorkState.document, F.document)
async def complete_work_document(message: types.Message, state: FSMContext):
    data = await state.get_data()
    if message.document is None:
        await message.answer(
            f"🆔 Ish ID: {data['work_id']}\n\n📄 Iltimos, hujjatni yuboring", reply_markup=back_keyboard()
        )

    await state.update_data(document_id=message.document.file_id)

    await state.set_state(CompleteWorkState.image)
    await message.answer("🖼 Endi rasm yuboring (agar bo‘lmasa, /skip yozing)")


@router.message(CompleteWorkState.image, F.photo)
async def complete_work_image(message: types.Message, state: FSMContext):
    photo_id = message.photo[-1].file_id
    await state.update_data(image_id=photo_id)

    await state.set_state(CompleteWorkState.explain)
    await message.answer("✍️ Ish bo‘yicha mijozga tushuncha berdingizmi?", reply_markup=ha_yoq_keyboard())


@router.message(CompleteWorkState.image, F.text == "/skip")
async def skip_image(message: types.Message, state: FSMContext):
    await state.update_data(image_id=None)

    await state.set_state(CompleteWorkState.explain)
    await message.answer("✍️ Ish bo‘yicha mijozga tushuncha berdingizmi?", reply_markup=ha_yoq_keyboard())


@router.callback_query(F.data.startswith("complete_ha_yoq:"), CompleteWorkState.explain)
async def complete_work_finish(callback: types.CallbackQuery, state: FSMContext):
    explain = callback.data.split(":")[1]
    if int(explain) == 1:
        data = await state.get_data()
        work_id = data.get("work_id")
        chat_id = data.get("chat_id")

        image_path = None
        if data.get("image_id"):
            image_path = await download_image(data["image_id"])

        document_path = None
        if data.get("document_id"):
            document_path = await download_image(data["document_id"])

        success = await complete_work(chat_id=chat_id, work_id=work_id, document_id=document_path, image_id=image_path)
        if success:
            await callback.message.answer(
                f"✅ Ish yakunlandi!\n\n"
                f"🆔 Ish ID: {work_id}\n"
                f"📝 Malumotlar saqlandi!\n\n"
            )
            return
        await callback.message.answer("❌ Malumotlarni yuklashda xatolik qayta harakat qilib ko'ring!", reply_markup=work_keyboard())
    else:
        await callback.message.answer("❌ Mijozga topshirilgan ish boyicha tushuncha berib qayta ishni yakunlashni bosing!", reply_markup=work_keyboard())

