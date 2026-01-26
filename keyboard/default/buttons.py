from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

back_button = KeyboardButton(text='Бекор қилиш')

car_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Элон бериш")], [KeyboardButton(text="Созламалар")]
    ],
    resize_keyboard=True
)

main_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="👤 Клиент"), KeyboardButton(text="🚖 Шофёр")]
    ],
    resize_keyboard=True
)

client_create_ad_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='Тошкентдан - Фарғонага'), KeyboardButton(text='Фарғонадан - Тошкентга')],
        [KeyboardButton(text='Почта бор')], [back_button]
    ],
    resize_keyboard=True
)

phone_markup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text='☎️ Телефон рақамингизни жўнатинг', request_contact=True)]
    ],
    resize_keyboard=True
)
