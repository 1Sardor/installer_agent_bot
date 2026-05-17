from aiogram import Router, types, filters
from aiogram.fsm.context import FSMContext
from aiogram import F

from handlers.api.public.has_unrated_work import get_unrated_work
from keyboard.default.public_buttons import phone_button, main_markup, standard_keyboard, satisfaction_keyboard
from utils.filters import IsNotStaff
from state.public_state import RegisterState, RatingState
from handlers.api.public.check_client import get_client
from handlers.api.public.connect_chat_id import connect_api
from handlers.api.public.rate import save_rating

router = Router()
router.message.filter(IsNotStaff())


@router.message(filters.CommandStart())
async def start(message: types.Message, state: FSMContext) -> None:
    checked = await get_client(message.chat.id)
    if checked:
        await message.answer('Assalomu alaykum Adnis botiga hush kelibsiz!', reply_markup=main_markup())

        unrated_work = await get_unrated_work(message.chat.id)

        if unrated_work:
            work = unrated_work[0]
            await state.update_data(unrated_works=unrated_work, current_index=0)
            await ask_standard_question(message, state, work)
        return

    await message.answer(
        'Assalomu alaykum Adnis botiga hush kelibsiz!\nBotdan foydalanish uchun telefon raqamingizni yuboring!',
        reply_markup=phone_button())
    await state.set_state(RegisterState.waiting_phone)


async def ask_standard_question(message: types.Message, state: FSMContext, work: dict):
    text = (
        f"№: #{work['id']}\nIsh turi: {work['work_type']}\nAgent: {work.get('user_name', 'N/A')}\n\n"
        f"1. Ishlarni to'liq holatda Eslatmalar xatida ko'rsatilgan "
        f"Standartlar bo'yicha ishingizni topshirib berdimi?"
    )
    if work.get('document'):
        await message.answer_document(document=work['document'], caption=text, reply_markup=standard_keyboard())
    else:
        await message.answer(text, reply_markup=standard_keyboard())
    await state.set_state(RatingState.waiting_standard)


@router.message(RegisterState.waiting_phone, F.contact)
async def phone_handler(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number.replace("+998", "")
    if phone.startswith("998"):
        phone = phone[3:]

    user = await connect_api(phone, message.chat.id)

    if not user:
        await message.answer("❌ Sizning raqamingiz bazada topilmadi.")
        await state.clear()
        return

    await message.answer("✅ Siz muvoffaqqiyatli royhatdan o'tdingiz!", reply_markup=main_markup())

    unrated_work = await get_unrated_work(message.chat.id)

    if unrated_work:
        work = unrated_work[0]
        await state.update_data(unrated_works=unrated_work, current_index=0)
        await ask_standard_question(message, state, work)
        return

    await state.clear()


@router.message(RatingState.waiting_standard, F.text.in_(["✅ HA", "❌ YOQ"]))
async def standard_handler(message: types.Message, state: FSMContext):
    await state.update_data(standard_answer=message.text)
    await message.answer(
        "2. Installerimiz xizmatidan mamnunmisiz?",
        reply_markup=satisfaction_keyboard()
    )
    await state.set_state(RatingState.waiting_satisfaction)


@router.message(RatingState.waiting_satisfaction, F.text.in_(["👎 Yoqmadi", "👍 O'rtacha", "🌟 A'lo"]))
async def satisfaction_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    unrated_works = data.get("unrated_works", [])
    current_index = data.get("current_index", 0)
    standard_answer = data.get("standard_answer", "")

    satisfaction_map = {"👎 Yoqmadi": -5, "👍 O'rtacha": 0, "🌟 A'lo": 1}
    rating = satisfaction_map[message.text]

    work = unrated_works[current_index]
    await save_rating(client_id=message.chat.id, standard_answer=standard_answer, rating=rating, work_id=work['id'])

    await message.answer("✅ Rahmat! Bahoyingiz qabul qilindi.", reply_markup=main_markup())

    next_index = current_index + 1
    if next_index < len(unrated_works):
        await state.update_data(current_index=next_index)
        await ask_standard_question(message, state, unrated_works[next_index])
    else:
        await state.clear()


@router.message(F.text == "📞 Kontakt")
async def contact_handler(message: types.Message):
    await message.answer(
        "👤 CEO: Adnis Islombek\n"
        "📲 Telegram: @Adnis_Islombek"
    )
