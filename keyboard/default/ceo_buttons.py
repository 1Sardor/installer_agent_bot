from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="💼 Ish"),
            ],
            [
                KeyboardButton(text="📊 Statistika"),
                KeyboardButton(text="⚡ Faol Ishlar")
            ],
            [
                KeyboardButton(text="💸 Razxod"),
                KeyboardButton(text="🎁 Bonus"),
            ],
            [
                KeyboardButton(text="👥 Hodimlar"),
                KeyboardButton(text="🧑‍🤝‍🧑 Klientlar")
            ]
        ],
        resize_keyboard=True
    )

def hodim_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Yangi Hodim")],
            [KeyboardButton(text="📋 Hodimlar ro'yxati"), KeyboardButton(text="⬅️ Orqaga")]
        ],
        resize_keyboard=True
    )


def hodim_status_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👑 Ceo")],
            [KeyboardButton(text="🧑‍💼 Agent")],
            [KeyboardButton(text="🛒 Seller")],
        ],
        resize_keyboard=True
    )


def client_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Yangi Klient")],
            [KeyboardButton(text="📋 Klientlar ro'yxati"), KeyboardButton(text="⬅️ Orqaga")]
        ],
        resize_keyboard=True
    )


def razxod_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="➕ Yangi Razxod")],
            [KeyboardButton(text="📋 Razxodlar ro'yxati"), KeyboardButton(text="⬅️ Orqaga")]
        ],
        resize_keyboard=True
    )
