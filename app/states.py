from aiogram.fsm.state import State, StatesGroup


class Reg(StatesGroup):
    """Далее прописываются состояния(этапы) которые должен пройти пользователь"""
    name = State()
    number = State()
    photo = State()
