from aiogram.fsm.state import StatesGroup, State


class ApplicationStatesGroup(StatesGroup):
    enter_responsible = State()
    enter_comments = State()
    enter_amount = State()
    enter_article = State()
    enter_payment_date = State()
    enter_add_info = State()
    enter_file = State()