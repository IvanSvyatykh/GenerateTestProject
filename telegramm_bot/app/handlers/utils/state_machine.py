from aiogram.fsm.state import StatesGroup, State


class QuestionStateMachine(StatesGroup):
    manual_subject = State()
    manual_grade = State()
    subject = State()
    theme = State()
    grade = State()
    format_response = State()
    question_num = State()
    percent_format_response = State()
    answer_num = State()
    file_format = State()
    generation_time = State()