from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def rating_keyboard(work_id):
    keyboard = [
        [
            InlineKeyboardButton(text="⭐", callback_data=f"rate_1_{work_id}"),
        ],
        [
            InlineKeyboardButton(text="⭐⭐", callback_data=f"rate_2_{work_id}"),
        ],
        [
            InlineKeyboardButton(text="⭐⭐⭐", callback_data=f"rate_3_{work_id}"),
        ],
        [
            InlineKeyboardButton(text="⭐⭐⭐⭐", callback_data=f"rate_4_{work_id}"),
        ],
        [
            InlineKeyboardButton(text="⭐⭐⭐⭐⭐", callback_data=f"rate_5_{work_id}"),
        ]
    ]

    return InlineKeyboardMarkup(inline_keyboard=keyboard)
