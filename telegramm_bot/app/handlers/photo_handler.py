from aiogram import Bot, Router, types,F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile
from utils.answers import GREETING_MESS
from service.recognize_photo_service import recognize_photo
router = Router()


@router.message("start")
async def start_dialog(message: types.Message, state: FSMContext):
    await message.answer(text=GREETING_MESS)



@router.message(F.photo)
async def get_photo_from_user(message: types.Message, state: FSMContext):
    await message.answer(text=GREETING_MESS)
    photo_path = f"./images/{message.from_user.id}.png"
    await message.bot.download(file=message.photo[-1].file_id, destination=photo_path)
    await recognize_photo()