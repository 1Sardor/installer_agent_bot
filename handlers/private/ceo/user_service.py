from aiogram import Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F

from handlers.api.ceo.user_api import get_user_list, create_user, update_user, user_delete
from keyboard.default.buttons import back_keyboard
from keyboard.default.ceo_buttons import hodim_keyboard, main_keyboard, hodim_status_keyboard
from keyboard.inline.ceo_buttons import hodim_inline_kb, edit_field_inline_kb, hodim_status_inline_kb
from state.ceo_state import AddHodimState, EditHodimState
from utils.filters import IsCeo

router = Router()
router.message.filter(IsCeo())


@router.message(lambda m: m.text == "👥 Hodimlar")
async def show_hodimlar_menu(message: Message):
    await message.answer("Hodimlar bo'limi:", reply_markup=hodim_keyboard())


@router.message(lambda m: m.text == "📋 Hodimlar ro'yxati")
async def list_hodimlar(message: Message):
    data = await get_user_list()

    if not data:
        await message.answer("Hodimlar hali qo'shilmagan.")
        return

    for count, u in enumerate(data, start=1):

        text = (
            f"📌 № <b>{count}</b>\n"
            f"👤 FIO: <b>{u.get('full_name', '-')}</b>\n"
            f"🆔 Chat ID: <b>{u.get('chat_id', '-')}</b>\n"
            f"🛡️ Role: <b>{u.get('status')}</b>\n"
        )

        await message.answer(
            text,
            reply_markup=hodim_inline_kb(u['id']),
            parse_mode="HTML"
        )

@router.message(lambda m: m.text == "➕ Yangi Hodim")
async def add_hodim_start(message: Message, state: FSMContext):
    await state.set_state(AddHodimState.full_name)
    await message.answer(
        "Iltimos, hodimning *FIO* ni kiriting:",
        parse_mode="Markdown",
        reply_markup=back_keyboard()
    )

@router.message(AddHodimState.full_name)
async def add_hodim_full_name(message: Message, state: FSMContext):
    full_name = message.text.strip()

    await state.update_data(full_name=full_name)

    await state.set_state(AddHodimState.chat_id)

    await message.answer(
        "Hodimni telegram *Chat id* sini kiriting:",
        reply_markup=back_keyboard(),
        parse_mode="Markdown"
    )


@router.message(AddHodimState.chat_id)
async def add_hodim_chat_id(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("Chat Id faqat raqamdan iborat bolishi kerak!")

    await state.update_data(chat_id=int(message.text))
    await state.set_state(AddHodimState.status)

    await message.answer(
        "Hodim rolini tanlang:",
        reply_markup=hodim_status_keyboard()
    )


@router.message(AddHodimState.status)
async def add_hodim_finish(message: Message, state: FSMContext):
    STATUS_MAP = {
        "👑 Ceo": 1,
        "🧑‍💼 Agent": 2,
        "🛒 Seller": 3,
    }
    if message.text not in STATUS_MAP:
        await message.answer("❌ Iltimos, tugmalardan birini tanlang")
        return

    data = await state.get_data()
    full_name = data["full_name"]
    chat_id = data["chat_id"]
    status = STATUS_MAP[message.text]

    success = await create_user(full_name=full_name, chat_id=chat_id, status=status)
    if not success:
        await message.answer("Hodim qo'shishda xatolik qayta urunib ko'ring!", reply_markup=hodim_keyboard())
        return

    await state.clear()

    await message.answer(
        f"✅ Hodim muvaffaqiyatli qo‘shildi!\n\n"
        f"👤 FIO: <b>{full_name}</b>\n"
        f"🆔 Chat Id: <b>{chat_id}</b>\n"
        f"🛡️ Status: <b>{message.text}</b>",
        reply_markup=hodim_keyboard()
    )


@router.callback_query(F.data.startswith("hodim_edit:"))
async def hodim_edit_cb(call: CallbackQuery, state: FSMContext):
    hodim_id = int(call.data.split(":")[1])

    await state.update_data(hodim_id=hodim_id)
    await state.set_state(EditHodimState.choose_field)

    await call.message.answer(
        "Nimani tahrirlaysiz?",
        reply_markup=edit_field_inline_kb()
    )
    await call.answer()


@router.callback_query(F.data.startswith("edit_field:"))
async def choose_edit_field(call: CallbackQuery, state: FSMContext):
    field = call.data.split(":")[1]

    if field == "full_name":
        await state.set_state(EditHodimState.full_name)
        await call.message.answer("Yangi full name kiriting:")

    elif field == "chat_id":
        await state.set_state(EditHodimState.chat_id)
        await call.message.answer("Yangi chat_id kiriting:")

    elif field == "status":
        await state.set_state(EditHodimState.status)
        await call.message.answer(
            "Yangi statusni tanlang:",
            reply_markup=hodim_status_inline_kb()
        )

    await call.answer()

@router.message(EditHodimState.full_name)
async def update_full_name(message: Message, state: FSMContext):
    data = await state.get_data()

    response = await update_user(
        user_id=data["hodim_id"],
        full_name=message.text
    )

    await state.clear()
    if not response:
        await message.answer("❌ Full nameni yangilashda xatolik")
    await message.answer("✅ Full name yangilandi")


@router.message(EditHodimState.chat_id)
async def update_chat_id(message: Message, state: FSMContext):
    if not message.text.isdigit():
        await message.answer("❌ Chat ID faqat raqam bo‘lishi kerak")
        return

    data = await state.get_data()

    response = await update_user(
        user_id=data["hodim_id"],
        chat_id=int(message.text)
    )

    await state.clear()
    if not response:
        await message.answer("❌ Chat ID yangilashda xatolik")
    await message.answer("✅ Chat ID yangilandi")


@router.callback_query(F.data.startswith("edit_status:"))
async def update_status(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    status = int(call.data.split(":")[1])

    await update_user(
        user_id=data["hodim_id"],
        status=status
    )

    await state.clear()
    if not status:
        await call.message.edit_text("❌ Status yangilashda xatolik")
    await call.message.edit_text("✅ Status yangilandi")
    await call.answer()


@router.callback_query(F.data.startswith("hodim_delete:"))
async def hodim_delete_cb(call: CallbackQuery):
    hodim_id = int(call.data.split(":")[1])

    success = await user_delete(hodim_id)
    if success:
        await call.message.edit_text("🗑 Hodim muvaffaqiyatli o‘chirildi")
    else:
        await call.message.answer("❌ Hodimni o‘chirishda xatolik yuz berdi")

    await call.answer()
