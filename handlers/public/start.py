from aiogram import Router, types, filters
from aiogram.fsm.context import FSMContext
from aiogram import F
from aiogram.types import FSInputFile

from handlers.api.public.has_unrated_work import get_unrated_work
from keyboard.default.public_buttons import phone_button
from utils.filters import IsNotStaff
from state.public_state import RegisterState
from keyboard.inline.public_button import rating_keyboard
from handlers.api.public.check_client import get_client
from handlers.api.public.connect_chat_id import connect_api
from handlers.api.public.rate import save_rating

router = Router()
router.message.filter(IsNotStaff())


@router.message(filters.CommandStart())
async def start(message: types.Message, state: FSMContext) -> None:
    checked = await get_client(message.chat.id)
    if checked:
        await message.answer('Assalomu alaykum Adnis botiga hush kelibsiz!')

        unrated_work = await get_unrated_work(message.chat.id)

        if unrated_work:
            for w in unrated_work:
                text = f"№: #{w['id']}\nIsh turi: {w['work_type']}\n\nIltimos ishni baxolang!"
                if w['document']:
                    await message.answer_document(
                        document=w['document'],
                        caption=text,
                        reply_markup=rating_keyboard(w['id'])
                    )
                else:
                    await message.answer(text, reply_markup=rating_keyboard(w['id']))
        return
    await message.answer(
        'Assalomu alaykum Adnis botiga hush kelibsiz!\nBotdan foydalanish uchun telefon raqamingizni yuboring!',
        reply_markup=phone_button())
    await state.set_state(RegisterState.waiting_phone)


@router.message(RegisterState.waiting_phone, F.contact)
async def phone_handler(message: types.Message, state: FSMContext):
    phone = message.contact.phone_number

    user = await connect_api(phone, message.chat.id)

    if not user:
        await message.answer("❌ Sizning raqamingiz bazada topilmadi.")
        await state.clear()
        return
    else:
        await message.answer("✅ Siz muvoffaqqiyatli royhatdan o'tdingiz!")

    unrated_work = await get_unrated_work(message.chat.id)

    if unrated_work:
        for w in unrated_work:
            text = f"№: #{w['id']}\nIsh turi: {w['work_type']}\n\nIltimos ishni baxolang!"
            if w['document']:
                await message.answer_document(
                    document=w['document'],
                    caption=text,
                    reply_markup=rating_keyboard(w['id'])
                )
            else:
                await message.answer(text, reply_markup=rating_keyboard(w['id']))

    await state.clear()


@router.callback_query(
    F.data.startswith("rate_")
)
async def rating_callback(callback: types.CallbackQuery, state: FSMContext):
    rating = int(callback.data.split("_")[1])
    work_id = int(callback.data.split("_")[2])
    client_id = callback.from_user.id

    await save_rating(client_id=client_id, rating=rating, work_id=work_id)

    await callback.message.edit_caption(
        caption=f"✅ Rahmat! Siz {rating} ⭐ baho berdingiz."
    )

    await callback.answer()
    await state.clear()
