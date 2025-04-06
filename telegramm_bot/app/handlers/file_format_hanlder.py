import os

from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InputFile
from handlers.utils.state_machine import QuestionStateMachine
from aiogram.types.input_file import FSInputFile
from service.file_generator import (
    generate_docx,
    generate_pdf,
    generate_excel,
)
from handlers.utils.keyboards import get_new_generate_keyboard

router = Router()


@router.callback_query(lambda c: c.data.startswith("file_format_"), QuestionStateMachine.file_format)
async def file_format_handler(callback_query: CallbackQuery, state: FSMContext):
    file_format = callback_query.data.split("_")[2]
    data = await state.get_data()
    test_json = data.get("test_json")
    subject = data.get("subject")

    if file_format == "docx":
        file_path = await generate_docx(test_json, subject, callback_query.from_user.id)
    elif file_format == "pdf":
        file_path = await generate_pdf(test_json, subject, callback_query.from_user.id)
    elif file_format == "excel":
        file_path = await generate_excel(test_json, subject, callback_query.from_user.id)

    with open(file_path, 'rb'):
        document = FSInputFile(file_path, filename=os.path.basename(file_path))

    await callback_query.message.answer_document(
        document=document,
        caption=f"Тест в формате {file_format.upper()}",
        reply_markup=await get_new_generate_keyboard()
    )

    await state.clear()
