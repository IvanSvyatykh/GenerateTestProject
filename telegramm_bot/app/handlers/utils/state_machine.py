from aiogram.fsm.state import StatesGroup, State


class QuestionStateMachine(StatesGroup):
    subject_area = State()
    subject = State()
    theme = State()
    complexity = State()
    format_response = State()
    question_num = State()
    percent_format_response = State()
    answer_num = State()
    file_format = State()