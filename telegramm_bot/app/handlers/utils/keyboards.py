from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

SUBJECT_AREAS = {
    "languages": [
        "🇷🇺 Русский язык",
        "📖 Литература",
        "🇬🇧 Английский язык",
        "🇩🇪 Немецкий язык",
        "🇫🇷 Французский язык",
    ],
    "math": [
        "➕ Математика",
        "📐 Алгебра",
        "📏 Геометрия",
        "💻 Информатика",
    ],
    "social": [
        "📜 История",
        "🏛️ Обществознание",
        "⚖️ Право",
        "💰 Экономика",
    ],
    "science": [
        "🔌 Физика",
        "⚗️ Химия",
        "🧬 Биология",
        "🗺️ География",
        "🌌 Астрономия",
    ],
    "art": [
        "🎼 Музыка",
        "🖼️ ИЗО",
        "🌐 МХК",
    ],
    "tech": [
        "🔧 Технология",
        "🤖 Робототехника",
        "🪚 Труд",
    ],
    "personal": [
        "🚨 ОБЖ",
        "🕊️ ОРКИСЭ",
    ],
}


async def get_area_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📚 Языки и литература", callback_data="area_languages")],
        [InlineKeyboardButton(text="🔢 Математика и информатика", callback_data="area_math")],
        [InlineKeyboardButton(text="🌍 Общественные науки", callback_data="area_social")],
        [InlineKeyboardButton(text="🔬 Естественные науки", callback_data="area_science")],
        [InlineKeyboardButton(text="🎨 Искусство и культура", callback_data="area_art")],
        [InlineKeyboardButton(text="🛠️ Технология", callback_data="area_tech")],
        [InlineKeyboardButton(text="🧠 Личностное развитие", callback_data="area_personal")],
        [InlineKeyboardButton(text="✍🏻 Ввести предметную область вручную", callback_data="manual_area")],
    ])


async def get_subject_keyboard(area_key: str) -> InlineKeyboardMarkup:
    subjects = SUBJECT_AREAS.get(area_key, [])
    keyboard = [
        [InlineKeyboardButton(text=subj, callback_data=f"subject_{subj}")]
        for subj in subjects
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_complexity_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔹 Легкий", callback_data="complexity_easy")],
        [InlineKeyboardButton(text="🔸 Средний", callback_data="complexity_medium")],
        [InlineKeyboardButton(text="🔺 Сложный", callback_data="complexity_hard")],
    ])


async def get_format_response_keyboard() -> InlineKeyboardMarkup:
    # Надо изменить промт для этих функций
    return InlineKeyboardMarkup(inline_keyboard=[
        #[InlineKeyboardButton(text="📜 Открытые вопросы", callback_data="format_open")],
        [InlineKeyboardButton(text="✅ Варианты ответов", callback_data="format_choices")],
        #[InlineKeyboardButton(text="🔀 Смешанный", callback_data="format_mixed")],
    ])


async def get_question_num_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="5 вопросов", callback_data="question_num_5")],
        [InlineKeyboardButton(text="10 вопросов", callback_data="question_num_10")],
        [InlineKeyboardButton(text="15 вопросов", callback_data="question_num_15")],
        [InlineKeyboardButton(text="20 вопросов", callback_data="question_num_15")],
        #[InlineKeyboardButton(text="Ввести вручную", callback_data="ignore")],
    ])


async def get_answer_question_num_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="2", callback_data="answer_question_num_2"),
         InlineKeyboardButton(text="3", callback_data="answer_question_num_3"),
         InlineKeyboardButton(text="4", callback_data="answer_question_num_4")],
    ])


async def get_mixed_format_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="~30% открытых", callback_data="mixed_percent_30")],
        [InlineKeyboardButton(text="~50% открытых", callback_data="mixed_percent_50")],
        [InlineKeyboardButton(text="~70% открытых", callback_data="mixed_percent_70")],
    ])


async def get_file_format_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🔵 Docx", callback_data="file_format_docx")],
        [InlineKeyboardButton(text="🔴 PDF", callback_data="file_format_pdf")],
        [InlineKeyboardButton(text="🟢 Excel", callback_data="file_format_excel")],
    ])
