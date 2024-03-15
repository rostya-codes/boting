from aiogram.types import KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

data = ('Nike', 'Adidas', 'Reebok')


def get_brands():
    """To unpack data from tuple. Returns keyboard"""
    keyboard = ReplyKeyboardBuilder()
    for brand in data:
        keyboard.add(KeyboardButton(text=brand))
    return keyboard.adjust(2).as_markup()
