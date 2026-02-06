from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💼 Ish"),
            ],
            [
                KeyboardButton(text="⚡ Faol Ishlar")
            ]
        ],
        resize_keyboard=True
    )

def work_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Yangi Ish")],
            [KeyboardButton(text="📋 Ishlar ro'yxati"), KeyboardButton(text="⬅️ Orqaga")]
        ],
        resize_keyboard=True
    )

