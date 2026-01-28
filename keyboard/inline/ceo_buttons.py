from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def hodim_inline_kb(hodim_id: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="✏️ Tahrirlash",
                    callback_data=f"hodim_edit:{hodim_id}"
                ),
                InlineKeyboardButton(
                    text="🗑 O‘chirish",
                    callback_data=f"hodim_delete:{hodim_id}"
                ),
            ]
        ]
    )


def edit_field_inline_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="👤 Full name", callback_data="edit_field:full_name")],
            [InlineKeyboardButton(text="🆔 Chat ID", callback_data="edit_field:chat_id")],
            [InlineKeyboardButton(text="🎭 Status", callback_data="edit_field:status")],
        ]
    )


def hodim_status_inline_kb():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="👑 CEO", callback_data="edit_status:1"),
                InlineKeyboardButton(text="🧑‍💼 Agent", callback_data="edit_status:2"),
                InlineKeyboardButton(text="🛒 Seller", callback_data="edit_status:3"),
            ]
        ]
    )
