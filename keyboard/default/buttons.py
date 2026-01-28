from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def back_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="⬅️ Orqaga")]
        ],
        resize_keyboard=True
    )
