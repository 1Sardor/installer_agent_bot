import time
from aiogram import Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F

from handlers.views import download_image
from keyboard.default.buttons import back_keyboard
from keyboard.default.ceo_buttons import razxod_keyboard
from keyboard.inline.ceo_buttons import confirm_inline_keyboard
from state.ceo_state import AddRazxodState
from utils.filters import IsAgent
from handlers.api.ceo.razxod_api import get_razxod_list, create_razxod

router = Router()
router.message.filter(IsAgent())


@router.message(lambda m: m.text == "💸 Razxod")
async def show_razxod_menu(message: Message):
    await message.answer("Razxodlar bo'limi:", reply_markup=razxod_keyboard())


@router.message(lambda m: m.text == "📋 Razxodlar ro'yxati")
async def list_hodimlar(message: Message):
    data = await get_razxod_list()

    if not data:
        await message.answer("Razxodlar hali qo'shilmagan.")
        return

    for count, u in enumerate(data, start=1):

        text = (
            f"📌 № <b>{count}</b>\n"
            f"👤 User: <b>{u.get('user_name', '-')}</b>\n"
            f"👤 Miqdor: <b>{u.get('miqdor', '-'):,}</b>\n"
            f"☎️ Izoh: <b>{u.get('izoh', '-')}</b>\n"
            f"📍 Yaratilgan sana: <b>{u.get('created_at')}</b>\n"
        )

        await message.answer(
            text,
            parse_mode="HTML"
        )
        time.sleep(0.05)


@router.message(lambda m: m.text == "➕ Yangi Razxod")
async def add_hodim_start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("💸 Xarajat miqdorini kiriting:", reply_markup=back_keyboard())
    await state.set_state(AddRazxodState.miqdor)


@router.message(AddRazxodState.miqdor)
async def get_miqdor(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❗️Faqat raqam kiriting. Masalan: 150000")
        return

    await state.update_data(miqdor=int(message.text))
    await message.answer("📝 Izoh kiriting:")
    await state.set_state(AddRazxodState.izoh)


@router.message(AddRazxodState.izoh)
async def get_izoh(message: Message, state: FSMContext):
    await state.update_data(izoh=message.text)
    await state.update_data(chat_id=message.chat.id)
    await message.answer(
        "🖼 Agar chek/rasm bo‘lsa yuboring.\n"
        "O‘tkazib yuborish uchun 👉 /skip"
    )
    await state.set_state(AddRazxodState.image)

@router.message(AddRazxodState.image)
async def handle_image(message: Message, state: FSMContext):
    # 1️⃣ Skip
    if message.text == "/skip":
        await state.update_data(image=None)
        await go_to_confirm(message, state)
        return

    # 2️⃣ Photo
    if message.photo:
        await state.update_data(
            image=message.photo[-1].file_id
        )
        await go_to_confirm(message, state)
        return

    await message.answer(
        "❗️Iltimos rasm yuboring yoki /skip yozing"
    )

async def go_to_confirm(message: Message, state: FSMContext):
    data = await state.get_data()

    text = (
        "🧾 Kiritilgan ma’lumotlarni tekshiring:\n\n"
        f"💸 Miqdor: <b>{data['miqdor']:,}</b>\n"
        f"📝 Izoh: <b>{data['izoh']}</b>\n"
        f"🖼 Rasm: <b>{'mavjud' if data.get('image') else 'yo‘q'}</b>\n\n"
        "✅ To‘g‘rimi?"
    )

    if data.get("image"):
        await message.answer_photo(
            photo=data["image"],
            caption=text,
            reply_markup=confirm_inline_keyboard(),
            parse_mode="HTML"
        )
    else:
        await message.answer(
            text,
            reply_markup=confirm_inline_keyboard(),
            parse_mode="HTML"
        )

    await state.set_state(AddRazxodState.is_correct)



@router.callback_query(
    AddRazxodState.is_correct,
    F.data == "razxod_confirm"
)
async def confirm_razxod(cb: CallbackQuery, state: FSMContext):
    data = await state.get_data()

    image_path = None
    if data.get("image"):
        image_path = await download_image(data["image"])

    success = await create_razxod(chat_id=data.get('chat_id'), miqdor=data.get("miqdor"), izoh=data.get("izoh"), image=image_path)
    if not success:
        await cb.message.answer("Xarajat qo'shishda xatolik qayta urunib ko'ring!", reply_markup=razxod_keyboard())
        return

    await cb.message.edit_reply_markup()
    await cb.message.answer("✅ Xarajat saqlandi!", reply_markup=razxod_keyboard())
    await state.clear()
    await cb.answer()


@router.callback_query(
    AddRazxodState.is_correct,
    F.data == "razxod_cancel"
)
async def cancel_razxod(cb: CallbackQuery, state: FSMContext):
    await cb.message.edit_reply_markup()
    await state.clear()
    await cb.message.answer("❌ Amal bekor qilindi", reply_markup=razxod_keyboard())
    await cb.answer()
