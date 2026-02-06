from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💼 Ish"),
            ],
            [
                KeyboardButton(text="📊 Statistika"),
                KeyboardButton(text="💸 Razxod"),
            ],
        ],
        resize_keyboard=True
    )


def work_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Yangi Ish")],
            [KeyboardButton(text="🛠 Mening ishlarim"), KeyboardButton(text="⚡ Faol Ishlar")],
            [KeyboardButton(text="📋 O'rnatilgan ishlar ro'yxati"), KeyboardButton(text="⬅️ Orqaga")]
        ],
        resize_keyboard=True
    )

