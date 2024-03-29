import logging

from aiogram import Bot, F, Router
from aiogram.enums import ChatAction
from aiogram.filters import Command, CommandObject, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, ContentType, Message
from aiogram.types.error_event import ErrorEvent

import app.builders as bld
import app.keyboards as kb
from app.middlewares import AdminProtect
from app.states import Reg

admin = Router()
router = Router()


# Создание логгера
logger = logging.getLogger(__name__)


@router.message(CommandStart(deep_link=True, magic=F.args.isdigit()))  # Сообщение об ошибке не будет выводиться
async def cmd_start(message: Message, command: CommandObject):  # Команда принимает все всё что угодно в ссылке
    """Answer to /start"""
    await message.reply('Hello!', reply_markup=kb.main)
    await message.answer('How are you?')
    await message.answer(f'Hello! You came from {command.args}')
    # await message.bot.send_message(chat_id=123, text='123')  # Первым аргументом указан получатель


@router.message(Command('id'))
async def get_user_id(message: Message):
    await message.answer(f'Your user tg id: {message.from_user.id}')


@router.message(F.photo)
async def get_photo(message: Message):
    """Send id of photo"""
    await message.reply(f'ID of photo: {message.photo[-1].file_id}')
    await message.bot.send_chat_action(
        chat_id=message.from_user.id,  # Обязательно нужно указать этот параметр
        action=ChatAction.UPLOAD_PHOTO  # action для отображения процесса загрузки какого-то действия
    )


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.reply(f'{message.from_user.first_name}, Do you need help?')
    await message.answer_photo(
        photo='https://external-content.duckduckgo.com/iu/?u=https%3A%2F%2Fs.yimg.com%2Fuu%2Fapi%2Fres%2F1.2%2FosColL8jvNaRXCddQ02_mw--~B%2FaD0xMDY3O3c9MTYwMDthcHBpZD15dGFjaHlvbg--%2Fhttps%3A%2F%2Fs.yimg.com%2Fuu%2Fapi%2Fres%2F1.2%2F4njf4qhU.A.ovzl3Q1E4bA--~B%2FaD0xMDY3O3c9MTYwMDthcHBpZD15dGFjaHlvbg--%2Fhttps%3A%2F%2Fo.aolcdn.com%2Fimages%2Fdims%3Fcrop%3D3341%252C2227%252C0%252C0%26quality%3D85%26format%3Djpg%26resize%3D1600%252C1067%26image_uri%3Dhttps%3A%2F%2Fs.yimg.com%2Fos%2Fcreatr-images%2F2019-03%2F59d8ef40-4f09-11e9-b1f7-457093f5389c%26client%3Da1acac3e1b3290917d92%26signature%3Dbdab94024a21889be72611a759d693048988c347.cf.jpg&f=1&nofb=1&ipt=42d4833a2c2a7b522c51edef771d36e4c30893caf52da4fefaa1f6a8c4eb4c85&ipo=images',
        caption='telegram photo')
    await message.answer(f'Your ID: {message.from_user.id}', reply_markup=kb.inline_main)


@router.message(Command('get_'))
async def cmd_get(message: Message, command: CommandObject):
    """Get argument and send it"""
    await message.answer(f'You entered get command with argument {command.args}')


@router.message(Command('get'))
async def cmd_get(message: Message, command: CommandObject):
    """Get more arguments and send it"""
    if not command.args:
        await message.reply('No args. You must to add args!')
        return
    try:
        value1, value2 = command.args.split(' ', maxsplit=1)
        await message.answer(f'You entered get command with:\nargument1 - {value1}\nargument1 - {value2}')
    except Exception:
        await message.reply('You sent incorrect args!')


@router.message(F.text == 'Basket')
async def basket(message: Message):
    await message.answer('Your cart is empty!')


@router.callback_query(F.data == 'basket')
async def basket(callback: CallbackQuery):
    await callback.answer('You selected basket', show_alert=True)
    await callback.message.answer('Your cart is empty!')


@router.message(Command('gb'))
async def get_keyboard_builder(message: Message):
    await message.answer('Keyboard builder:', reply_markup=bld.get_brands())


@router.message(Command('fsm'))
async def fsm_handler(message: Message, state: FSMContext):
    await state.set_state(Reg.name)  # Установка состояния Reg.name
    await message.answer(f'Hello! Enter your name')


@router.message(Reg.name)  # Ловим состояние name
async def reg_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)  # Поместить информацию в ячейку
    await state.set_state(Reg.number)
    await message.answer('Send your phone number')


@router.message(Reg.number)  # Ловим состояние number
async def reg_number(message: Message, state: FSMContext):
    await state.update_data(number=message.text)  # Поместить информацию в ячейку
    await state.set_state(Reg.photo)
    await message.answer('Send your photo')


@router.message(Reg.photo)  # Ловим состояние photo
async def reg_photo(message: Message, state: FSMContext):
    await state.update_data(photo=message.photo[-1].file_id)  # Поместить информацию в ячейку
    data = await state.get_data()  # Получить данные
    await message.answer_photo(photo=data['photo'],
                               caption=f'about you:\n'
                                       f'name: {data["name"]} | phone number: {data["number"]}')
    await state.clear()  # Очистка состояний


@router.message(Command('webapp'))
async def webapp_handler(message: Message):
    await message.answer('Opening youtube..', reply_markup=kb.open_youtube)


'''
@router.message(content_types=ContentType.DOCUMENT)
async def audio_handler(message: Message, bot: Bot):
    file_id = message.document.file_id
    photo_id = message.photo[-1].file_id
    file = await bot.get_file(file_id)
    file_path = file.file_path
    await bot.download_file(file_path, 'file.txt')
    # 2-cond way
    document = message.document
    await bot.download(document)
    #or
    await bot.download(message.document)
'''


@admin.message(AdminProtect(), Command('apanel'))
async def apanel_handler(message: Message):
    await message.answer('It\'s admin panel')


@router.error()
async def error_handler(event: ErrorEvent):
    logger.critical('Critical error: %s', event.exception, exc_info=True)
