import asyncio
from time import time
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from handlers.utils.state_machine import QuestionStateMachine
from api.utils.promt_builder import create_user_prompt
from api.rapid_gpt4_requests import gpt4_request
from handlers.utils.shared import loading_tasks
from handlers.utils.loading import animate_loading
from handlers.utils.answers import (
    ERROR_MESS,
    CHOOSE_SUBJECT_AREA,
    CHOOSE_SUBJECT,
    CHOOSE_THEME,
    CHOOSE_GRADE,
    CHOOSE_FORMAT_RESPONSE,
    CHOOSE_QUESTION_NUM,
    CHOOSE_ANSWER_NUM,
    CHOOSE_PERCENT_FORMAT_RESPONSE,
    CHOOSE_QUESTION_NUM_WITH_ANSWER_NUM,
    CHOOSE_QUESTION_NUM_WITH_ANSWER_NUM_AND_PERCENT,
    FINISHED_TEST,
    FINISHED_TEST_WITH_ANSWER_NUM,
    FINISHED_TEST_WITH_ANSWER_NUM_AND_PERCENT,
)
from handlers.question_handler import (
    SUBJECT_AREA_NAMES,
)
from handlers.utils.keyboards import (
    get_back_keyboard,
    get_class_keyboard,
    get_subject_keyboard,
)

router = Router()


@router.callback_query(lambda c: c.data == "back", QuestionStateMachine.theme)
async def step_to_subject(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    subject_area = data.get("subject_area")
    for key, value in SUBJECT_AREA_NAMES.items():
        if subject_area in value:
            subject_area = key
            break
    await state.set_state(QuestionStateMachine.subject)
    await callback_query.message.edit_text(
        text=CHOOSE_SUBJECT.format(subject_area=SUBJECT_AREA_NAMES[subject_area]),
        parse_mode="Markdown",
        reply_markup=await get_subject_keyboard(subject_area),
    )


@router.callback_query(lambda c: c.data == "back", QuestionStateMachine.grade)
async def step_to_theme(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(QuestionStateMachine.theme)
    data = await state.get_data()
    subject_area = data.get("subject_area")
    subject = data.get("subject")
    await state.update_data(bot_message_id=callback_query.message.message_id)
    await callback_query.message.edit_text(
        text=CHOOSE_THEME.format(subject_area=subject_area, subject=subject),
        parse_mode="Markdown",
        reply_markup=await get_back_keyboard(),
    )


@router.callback_query(lambda c: c.data == "back", QuestionStateMachine.format_response)
async def step_to_grade(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(QuestionStateMachine.grade)
    data = await state.get_data()
    subject_area = data.get("subject_area")
    subject = data.get("subject")
    theme = data.get("theme")
    await state.update_data(bot_message_id=callback_query.message.message_id)
    await callback_query.message.edit_text(
        text=CHOOSE_GRADE.format(
            subject_area=subject_area, subject=subject, theme=theme
        ),
        parse_mode="Markdown",
        reply_markup=await get_class_keyboard(subject_area),
    )
