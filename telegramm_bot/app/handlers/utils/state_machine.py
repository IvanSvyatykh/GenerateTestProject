from aiogram.fsm.state import StatesGroup, State


class QuestionStateMachine(StatesGroup):
    subject = State()
    theme = State()
    question_num = State()
    question_type = State()
