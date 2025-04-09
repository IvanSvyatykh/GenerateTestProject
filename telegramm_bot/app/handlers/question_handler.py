import asyncio
import json
from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from aiohttp import ClientSession
from handlers.utils.state_machine import QuestionStateMachine
from api.utils.promt_builder import create_user_prompt
from api.utils.response_validate import validate_json
from api.rapid_gpt4_requests import gpt4_request
from handlers.utils.shared import loading_tasks
from handlers.utils.loading import animate_loading
from handlers.utils.answers import (
    ERROR_MESS,
    CHOOSE_SUBJECT_AREA,
    CHOOSE_SUBJECT,
    CHOOSE_THEME,
    CHOOSE_COMPLEXITY,
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
from handlers.utils.keyboards import (
    get_subject_keyboard,
    get_complexity_keyboard,
    get_format_response_keyboard,
    get_question_num_keyboard,
    get_answer_question_num_keyboard,
    get_mixed_format_keyboard,
    get_file_format_keyboard,
    get_area_keyboard,
    get_new_generate_keyboard,
)


router = Router()

SUBJECT_AREA_NAMES = {
    "languages": "📚 Языки и литература",
    "math": "🔢 Математика и информатика",
    "social": "🌍 Общественные науки",
    "science": "🔬 Естественные науки",
    "art": "🎨 Искусство и культура",
    "tech": "🛠️ Технология",
    "personal": "🧠 Личностное развитие"
}


@router.callback_query(lambda c: c.data == "new_test")
async def new_test_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(QuestionStateMachine.subject_area)

    await callback_query.message.answer(
        text=CHOOSE_SUBJECT_AREA,
        parse_mode="Markdown",
        reply_markup=await get_area_keyboard()
    )


@router.callback_query(lambda c: c.data.startswith("area_"), QuestionStateMachine.subject_area)
async def subject_area_handler(callback_query: CallbackQuery, state: FSMContext):
    subject_area = callback_query.data.split("_")[1]
    await state.update_data(subject_area=SUBJECT_AREA_NAMES[subject_area])
    await state.set_state(QuestionStateMachine.subject)

    await callback_query.message.edit_text(
        text=CHOOSE_SUBJECT.format(subject_area=SUBJECT_AREA_NAMES[subject_area]),
        parse_mode="Markdown",
        reply_markup=await get_subject_keyboard(subject_area),
    )


@router.callback_query(lambda c: c.data.startswith("subject_"), QuestionStateMachine.subject)
async def choose_subject_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    subject_area = data.get("subject_area")

    subject = callback_query.data.split("_")[1]
    await state.update_data(subject=subject)

    await state.update_data(bot_message_id=callback_query.message.message_id)

    await state.set_state(QuestionStateMachine.theme)
    await callback_query.message.edit_text(
        text=CHOOSE_THEME.format(
            subject_area=subject_area,
            subject=subject),
        parse_mode="Markdown",
    )


@router.message(F.text, QuestionStateMachine.theme)
async def choose_theme_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()
    subject_area = data.get("subject_area")
    subject = data.get("subject")

    theme = message.text
    await state.update_data(theme=theme)

    bot_message_id = data.get("bot_message_id")
    await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    await message.delete()

    await state.set_state(QuestionStateMachine.complexity)
    await message.answer(
        text=CHOOSE_COMPLEXITY.format(
            subject_area=subject_area,
            subject=subject,
            theme=theme),
        parse_mode="Markdown",
        reply_markup=await get_complexity_keyboard(),
    )


@router.callback_query(lambda c: c.data.startswith("complexity_"), QuestionStateMachine.complexity)
async def choose_complexity_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    subject_area = data.get("subject_area")
    subject = data.get("subject")
    theme = data.get("theme")

    complexity_names = {
        "easy": "🔹 Легкий",
        "medium": "🔸 Средний",
        "hard": "🔺 Сложный"
    }

    complexity = callback_query.data.split("_")[1]
    await state.update_data(complexity=complexity_names[complexity])

    await state.set_state(QuestionStateMachine.format_response)
    await callback_query.message.edit_text(
        text=CHOOSE_FORMAT_RESPONSE.format(
            subject_area=subject_area,
            subject=subject,
            theme=theme,
            complexity=complexity_names[complexity]),
        parse_mode="Markdown",
        reply_markup=await get_format_response_keyboard(),
    )


@router.callback_query(lambda c: c.data.startswith("format_"), QuestionStateMachine.format_response)
async def choose_format_response_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    subject_area = data.get("subject_area")
    subject = data.get("subject")
    theme = data.get("theme")
    complexity = data.get("complexity")

    format_names = {
        "open": "📜 Открытые вопросы",
        "choices": "✅ Варианты ответов",
        "mixed": "🔀 Смешанный"
    }

    format_response = callback_query.data.split("_")[1]
    await state.update_data(format_response=format_names[format_response])

    if format_response == "open":
        await state.set_state(QuestionStateMachine.question_num)
        await callback_query.message.edit_text(
            text=CHOOSE_QUESTION_NUM.format(
                subject_area=subject_area,
                subject=subject,
                theme=theme,
                complexity=complexity,
                format_response=format_names[format_response]),
            parse_mode="Markdown",
            reply_markup=await get_question_num_keyboard(),
        )
    else:
        await state.set_state(QuestionStateMachine.answer_num)
        await callback_query.message.edit_text(
            text=CHOOSE_ANSWER_NUM.format(
                subject_area=subject_area,
                subject=subject,
                theme=theme,
                complexity=complexity,
                format_response=format_names[format_response]),
            parse_mode="Markdown",
            reply_markup=await get_answer_question_num_keyboard(),
        )


@router.callback_query(lambda c: c.data.startswith("answer_question_num_"), QuestionStateMachine.answer_num)
async def choose_answer_question_num_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    subject_area = data.get("subject_area")
    subject = data.get("subject")
    theme = data.get("theme")
    complexity = data.get("complexity")
    format_response = data.get("format_response")

    answer_num = callback_query.data.split("_")[3]
    await state.update_data(answer_num=answer_num)
    if format_response == "✅ Варианты ответов":
        await state.set_state(QuestionStateMachine.question_num)
        await callback_query.message.edit_text(
            text=CHOOSE_QUESTION_NUM_WITH_ANSWER_NUM.format(
                subject_area=subject_area,
                subject=subject,
                theme=theme,
                complexity=complexity,
                format_response=format_response,
                answer_num=answer_num),
            parse_mode="Markdown",
            reply_markup=await get_question_num_keyboard(),
        )
    else:
        await state.set_state(QuestionStateMachine.percent_format_response)
        await callback_query.message.edit_text(
            text=CHOOSE_PERCENT_FORMAT_RESPONSE.format(
                subject_area=subject_area,
                subject=subject,
                theme=theme,
                complexity=complexity,
                format_response=format_response,
                answer_num=answer_num),
            parse_mode="Markdown",
            reply_markup=await get_mixed_format_keyboard(),
        )


@router.callback_query(lambda c: c.data.startswith("mixed_percent_"), QuestionStateMachine.percent_format_response)
async def choose_mixed_percent_handler(callback_query: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    subject_area = data.get("subject_area")
    subject = data.get("subject")
    theme = data.get("theme")
    complexity = data.get("complexity")
    format_response = data.get("format_response")
    answer_num = data.get("answer_num")

    mixed_percent = callback_query.data.split("_")[2]
    await state.update_data(mixed_percent=mixed_percent)

    await state.set_state(QuestionStateMachine.question_num)
    await callback_query.message.edit_text(
        text=CHOOSE_QUESTION_NUM_WITH_ANSWER_NUM_AND_PERCENT.format(
            subject_area=subject_area,
            subject=subject,
            theme=theme,
            complexity=complexity,
            format_response=format_response,
            answer_num=answer_num,
            mixed_percent=mixed_percent),
        parse_mode="Markdown",
        reply_markup=await get_question_num_keyboard(),
    )


@router.callback_query(lambda c: c.data.startswith("question_num_"), QuestionStateMachine.question_num)
async def finished_test_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.update_data(question_num=callback_query.data.split("_")[2])
    data = await state.get_data()

    subject_area = data.get("subject_area")
    subject = data.get("subject")
    theme = data.get("theme")
    complexity = data.get("complexity")
    format_response = data.get("format_response")
    answer_num = data.get("answer_num")
    mixed_percent = data.get("mixed_percent")
    question_num = data.get("question_num")

    if answer_num is None:
        finished_text = FINISHED_TEST.format(
            subject_area=subject_area,
            subject=subject,
            theme=theme,
            complexity=complexity,
            format_response=format_response,
            question_num=question_num,
        )
    elif mixed_percent is None:
        finished_text = FINISHED_TEST_WITH_ANSWER_NUM.format(
            subject_area=subject_area,
            subject=subject,
            theme=theme,
            complexity=complexity,
            format_response=format_response,
            answer_num=answer_num,
            question_num=question_num,
        )
    else:
        finished_text = FINISHED_TEST_WITH_ANSWER_NUM_AND_PERCENT.format(
            subject_area=subject_area,
            subject=subject,
            theme=theme,
            complexity=complexity,
            format_response=format_response,
            answer_num=answer_num,
            mixed_percent=mixed_percent,
            question_num=question_num,
        )

    loading_msg = await callback_query.message.edit_text(text="⏳ Генерирую тест")

    key = f"{callback_query.from_user.id}_{loading_msg.message_id}"
    loading_task = asyncio.create_task(
        animate_loading(callback_query.bot, loading_msg.chat.id, loading_msg.message_id, key)
    )
    loading_tasks[key] = loading_task

    user_prompt = create_user_prompt(data)
    response = await gpt4_request(user_prompt, format_response)

    if key in loading_tasks:
        loading_tasks[key].cancel()
        try:
            await loading_tasks[key]
        except asyncio.CancelledError:
            pass

    if "error" in response:
        await state.clear()
        await callback_query.message.edit_text(
            ERROR_MESS,
            parse_mode="Markdown",
            reply_markup=get_new_generate_keyboard(),
        )

    await state.update_data(test_json=response)
    await state.set_state(QuestionStateMachine.file_format)
    await callback_query.message.edit_text(
        text=finished_text,
        parse_mode="Markdown",
        reply_markup=await get_file_format_keyboard(),
    )
