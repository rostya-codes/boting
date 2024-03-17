from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup,
                           KeyboardButton, ReplyKeyboardMarkup, WebAppInfo)

main = ReplyKeyboardMarkup(keyboard=[
    # 👇 1 список = 1 ряд
    [
        KeyboardButton(text='Basket')
    ],
    [
        KeyboardButton(text='Contacts')
    ],
    [
        KeyboardButton(text='Send location', request_location=True)
    ],
    [
        KeyboardButton(text='Send contact', request_contact=True)
    ],
], resize_keyboard=True, one_time_keyboard=True, input_field_placeholder='Select point from menu...')


inline_main = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Basket', callback_data='basket')
    ],
    [
        InlineKeyboardButton(text='Catalog', callback_data='catalog')
    ],
    [
        InlineKeyboardButton(text='Contacts', callback_data='contacts')
    ],
])

open_youtube = InlineKeyboardMarkup(inline_keyboard=[
    [
        InlineKeyboardButton(text='Open YouTube', web_app=WebAppInfo(url='https://youtube.com'))
    ]
])
