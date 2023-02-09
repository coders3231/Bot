from aiogram.dispatcher.filters.state import StatesGroup, State


class TestState(StatesGroup):
    joined = State()
    checker = State()
    delete = State()