import os
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery
from handlers.utils.state_machine import QuestionStateMachine
from aiogram.types.input_file import FSInputFile
from service.file_generator import (
    generate_docx,
    generate_pdf,
    generate_excel,
)
from handlers.utils.keyboards import get_new_generate_keyboard
from database.repository import BotLogsRepository
from database.core import get_async_session
from time import time
from datetime import datetime

router = Router()


@router.callback_query(
    lambda c: c.data.startswith("file_format_"), QuestionStateMachine.file_format
)
async def file_format_handler(callback_query: CallbackQuery, state: FSMContext):
    file_format = callback_query.data.split("_")[2]
    data = await state.get_data()
    test_json = data.get("test_json")
    theme = data.get("theme")
    format_response = data.get("format_response")

    if file_format == "docx":
        file_path = await generate_docx(
            test_json, theme, callback_query.from_user.id, format_response
        )
    elif file_format == "pdf":
        file_path = await generate_pdf(
            test_json, theme, callback_query.from_user.id, format_response
        )
    elif file_format == "excel":
        file_path = await generate_excel(
            test_json, theme, callback_query.from_user.id, format_response
        )

    with open(file_path, "rb"):
        document = FSInputFile(file_path, filename=os.path.basename(file_path))
    print("Log to db")
    async with get_async_session() as db_session:
        print("start logging...")
        subject = (
            data.get("subject")
            if data.get("subject") is not None
            else data.get("manual_subject")
        )
        logs_repo = BotLogsRepository(db_session)
        log = {
            "user_id": callback_query.from_user.id,
            "test_theme": subject,
            "test_name": data.get("theme"),
            "generation_time": int(data.get("generation_time")),
            "question_num": int(data.get("question_num")),
            "date": datetime.now(),
        }
        await logs_repo.add_log(log)
        print("end logging ...")
    await callback_query.message.answer_document(
        document=document,
        caption=f"Тест в формате {file_format.upper()}",
        reply_markup=await get_new_generate_keyboard(),
    )

    await state.clear()
