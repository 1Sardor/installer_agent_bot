from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def accept_work_inline_keyboard(work_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Ishni qabul qilish",
                    callback_data=f"accept_work:{work_id}"
                )
            ]
        ]
    )


def complete_work_inline_keyboard(work_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Ishni tugatildi",
                    callback_data=f"complete_work:{work_id}"
                )
            ]
        ]
    )


def ha_yoq_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✅ Ha",
                    callback_data=f"complete_ha_yoq:1"
                ),
                InlineKeyboardButton(
                    text="❌ Yoq",
                    callback_data=f"complete_ha_yoq:0"
                ),
            ]
        ]
    )