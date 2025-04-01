from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from handlers.utils.answers import (
    GREETING_MESS,
    CHOOSE_SUBJECT,
    CHOOSE_THEME,
    CHOOSE_QUESTION_NUM,
    CHOOSE_QUESTION_TYPE,
)
from service.generate_test import generate_test, TEMPLATE
from handlers.utils.state_machine import QuestionStateMachine

router = Router()


@router.message(Command("start"))
async def start_dialog(message: types.Message, state: FSMContext):
    await message.answer(text=GREETING_MESS)
    await state.set_state(QuestionStateMachine.subject)
    await message.answer(text=CHOOSE_SUBJECT)


@router.message(F.text, QuestionStateMachine.subject)
async def choose_subject(message: types.Message, state: FSMContext):
    await state.update_data(subject=message.text)
    await state.set_state(QuestionStateMachine.theme)
    await message.answer(text=CHOOSE_THEME)


@router.message(F.text, QuestionStateMachine.theme)
async def choose_theme(message: types.Message, state: FSMContext):
    await state.update_data(theme=message.text)
    await state.set_state(QuestionStateMachine.question_num)
    await message.answer(text=CHOOSE_QUESTION_NUM)


@router.message(F.text, QuestionStateMachine.question_num)
async def choose_question_num(message: types.Message, state: FSMContext):
    await state.update_data(question_num=message.text)
    await state.set_state(QuestionStateMachine.question_type)
    await message.answer(text=CHOOSE_QUESTION_TYPE)


@router.message(F.text, QuestionStateMachine.question_type)
async def choose_question_type(message: types.Message, state: FSMContext):
    await state.update_data(question_type=message.text)
    result = await state.get_data()
    await state.clear()
    test = await generate_test(
        TEMPLATE.format(
            result["subject"],
            result["theme"],
            result["question_num"],
            result["question_type"],
        )
    )
    await message.answer(text=str(test.choices[0].message.content))
