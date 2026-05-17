from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def phone_button():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📱 Telefon yuborish", request_contact=True)]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def main_markup():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Kontakt")]
        ],
        resize_keyboard=True
    )


def standard_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="✅ HA"), KeyboardButton(text="❌ YOQ")]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )


def satisfaction_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [
                KeyboardButton(text="👎 Yoqmadi"),
                KeyboardButton(text="👍 O'rtacha"),
                KeyboardButton(text="🌟 A'lo"),
            ]
        ],
        resize_keyboard=True,
        one_time_keyboard=True
    )
