from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def generate_button(user_id):
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text='User info',
                                     url=f'tg://user?id={user_id}')
            ]
        ]
    )


bot_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Заказ", url=f'tg://user?id=6796696901')
        ]
    ]
)

confirm_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Tasdiqlash', callback_data='confirm'),
            InlineKeyboardButton(text='Bekor qilish', callback_data='cancel'),

        ]
    ]
)
