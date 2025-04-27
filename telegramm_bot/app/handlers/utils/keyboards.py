from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

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

SUBJECT_GRADES = {
    "🇷🇺 Русский язык": list(range(1, 12 + 1)),
    "📖 Литература": list(range(5, 12 + 1)),
    "🇬🇧 Английский язык": list(range(2, 11 + 1)),
    "🇩🇪 Немецкий язык": list(range(5, 11 + 1)),
    "🇫🇷 Французский язык": list(range(5, 11 + 1)),

    "➕ Математика": list(range(1, 6)),
    "📐 Алгебра": list(range(7, 11 + 1)),
    "📏 Геометрия": list(range(7, 11 + 1)),
    "💻 Информатика": list(range(7, 11 + 1)),

    "📜 История": list(range(5, 11 + 1)),
    "🏛️ Обществознание": list(range(6, 11 + 1)),
    "⚖️ Право": list(range(9, 11 + 1)),
    "💰 Экономика": list(range(9, 11 + 1)),

    "🔌 Физика": list(range(7, 11 + 1)),
    "⚗️ Химия": list(range(8, 11 + 1)),
    "🧬 Биология": list(range(5, 11 + 1)),
    "🗺️ География": list(range(5, 10 + 1)),
    "🌌 Астрономия": [10, 11],

    "🎼 Музыка": list(range(1, 7 + 1)),
    "🖼️ ИЗО": list(range(1, 7 + 1)),
    "🌐 МХК": [10, 11],

    "🔧 Технология": list(range(5, 9 + 1)),
    "🤖 Робототехника": list(range(5, 11 + 1)),
    "🪚 Труд": list(range(1, 4 + 1)),

    "🚨 ОБЖ": list(range(8, 11 + 1)),
    "🕊️ ОРКИСЭ": [4],
}


async def get_new_generate_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Сгенерировать новый тест", callback_data="new_test")],
    ])


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


async def get_class_keyboard(subject: str) -> InlineKeyboardMarkup:
    available_classes = SUBJECT_GRADES.get(subject, list(range(1, 12 + 1)))

    sections = {
        "Начальная школа": [1, 2, 3, 4],
        "Средняя школа": [5, 6, 7, 8, 9],
        "Старшая школа": [10, 11],
    }

    keyboard = []
    for section, grades in sections.items():
        intersection = [g for g in grades if g in available_classes]
        if not intersection:
            continue
        keyboard.append([InlineKeyboardButton(text=section, callback_data=f"grade_block_{section}")])
        row = []
        for i, grade in enumerate(intersection, 1):
            row.append(InlineKeyboardButton(text=f"{grade} кл.", callback_data=f"grade_{grade}"))
            if i % 2 == 0:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
    keyboard.append([InlineKeyboardButton(text="✍🏻 Ввести сложность вручную", callback_data=f"manual_grade")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_format_response_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📜 Открытые вопросы", callback_data="format_open")],
        [InlineKeyboardButton(text="✅ Варианты ответов", callback_data="format_choices")],
        [InlineKeyboardButton(text="🔀 Смешанный", callback_data="format_mixed")],
        [InlineKeyboardButton(text="🔠 С пропусками", callback_data="format_pass")]
    ])


async def get_question_num_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="5 вопросов", callback_data="question_num_5")],
        [InlineKeyboardButton(text="10 вопросов", callback_data="question_num_10")],
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
