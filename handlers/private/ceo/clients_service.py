from aiogram import Router, types
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram import F

from keyboard.default.buttons import back_keyboard
from keyboard.default.ceo_buttons import client_keyboard
from state.ceo_state import AddClientState
from utils.filters import IsCeo
from handlers.api.ceo.client_api import get_client_list, create_client

router = Router()
router.message.filter(IsCeo())


@router.message(lambda m: m.text == "🧑‍🤝‍🧑 Klientlar")
async def show_clients_menu(message: Message):
    await message.answer("Klientlar bo'limi:", reply_markup=client_keyboard())


@router.message(lambda m: m.text == "📋 Klientlar ro'yxati")
async def list_clients(message: Message):
    data = await get_client_list()

    if not data:
        await message.answer("Klientlar hali qo'shilmagan.")
        return

    for count, u in enumerate(data, start=1):

        text = (
            f"📌 № <b>{count}</b>\n"
            f"👤 FIO: <b>{u.get('full_name', '-')}</b>\n"
            f"☎️ Telefon Raqam: <b>{u.get('phone', '-')}</b>\n"
            f"📍 Address: <b>{u.get('address')}</b>\n"
        )

        await message.answer(
            text,
            parse_mode="HTML"
        )


@router.message(lambda m: m.text == "➕ Yangi Klient")
async def add_client_start(message: Message, state: FSMContext):
    await state.set_state(AddClientState.full_name)
    await message.answer(
        "Iltimos, Klientning *FIO* ni kiriting:",
        parse_mode="Markdown",
        reply_markup=back_keyboard()
    )


@router.message(AddClientState.full_name)
async def get_full_name(message: Message, state: FSMContext):
    await state.update_data(full_name=message.text)
    await message.answer("📞 Telefon raqamini kiriting:")
    await state.set_state(AddClientState.phone)


@router.message(AddClientState.phone)
async def get_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer("📍 Manzilni kiriting:")
    await state.set_state(AddClientState.address)


@router.message(AddClientState.address)
async def get_address(message: Message, state: FSMContext):
    await state.update_data(address=message.text)

    data = await state.get_data()


    success = await create_client(full_name=data.get("full_name"), phone=data.get("phone"), address=data.get("address"))
    if not success:
        await message.answer("Hodim qo'shishda xatolik qayta urunib ko'ring!", reply_markup=client_keyboard())
        return


    await message.answer(
        "✅ Mijoz muvaffaqiyatli qo‘shildi!\n\n"
        f"👤 Ism: <b>{data['full_name']}</b>\n"
        f"☎️ Tel: <b>{data['phone']}</b>\n"
        f"📍 Manzil: <b>{data['address']}</b>"
    , parse_mode="HTML", reply_markup=client_keyboard())

    await state.clear()

