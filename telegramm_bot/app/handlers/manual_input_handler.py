from aiogram import Router, types, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from handlers.utils.state_machine import QuestionStateMachine
from handlers.utils.answers import (
    MANUAL_AREA,
    MANUAL_SUBJECT,
    CHOOSE_THEME,
)

router = Router()


@router.callback_query(lambda c: c.data == "manual_area", QuestionStateMachine.subject_area)
async def manual_subject_area_handler(callback_query: CallbackQuery, state: FSMContext):
    await state.set_state(QuestionStateMachine.manual_area)
    await state.update_data(bot_message_id=callback_query.message.message_id)

    await callback_query.message.edit_text(
        text=MANUAL_AREA,
        parse_mode="Markdown",
    )


@router.message(F.text, QuestionStateMachine.manual_area)
async def input_area_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()

    subject_area = message.text
    await state.update_data(subject_area=subject_area)

    bot_message_id = data.get("bot_message_id")
    await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    await message.delete()

    await state.set_state(QuestionStateMachine.manual_subject)
    bot_message = await message.answer(
        text=MANUAL_SUBJECT.format(subject_area=subject_area),
        parse_mode="Markdown",
    )
    await state.update_data(bot_message_id=bot_message.message_id)


@router.message(F.text, QuestionStateMachine.manual_subject)
async def input_subject_handler(message: types.Message, state: FSMContext):
    data = await state.get_data()

    subject_area = data.get("subject_area")
    subject = message.text
    await state.update_data(subject=subject)

    bot_message_id = data.get("bot_message_id")
    try:
        await message.bot.delete_message(chat_id=message.chat.id, message_id=bot_message_id)
    except Exception as e:
        print(f"⚠️ Не удалось удалить сообщение бота: {e}. {bot_message_id}")
    await message.delete()

    await state.set_state(QuestionStateMachine.theme)
    bot_message = await message.answer(
        text=CHOOSE_THEME.format(subject_area=subject_area, subject=subject),
        parse_mode="Markdown",
    )
    await state.update_data(bot_message_id=bot_message.message_id)

