from aiogram.fsm.state import StatesGroup, State


class AdminStatesGroup(StatesGroup):
    enter_id = State()