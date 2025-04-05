from aiogram import types, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from handlers.utils.state_machine import QuestionStateMachine
from handlers.utils.answers import GREETING_MESS
from handlers.utils.keyboards import get_area_keyboard

router = Router()


@router.message(Command("start"))
async def auth_handler(message: types.Message, state: FSMContext):
    await state.set_state(QuestionStateMachine.subject_area)
    await message.answer(
        text=GREETING_MESS,
        parse_mode="Markdown",
        reply_markup=await get_area_keyboard(),
    )
