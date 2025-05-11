from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

SUBJECT_AREAS = [
    "🇷🇺 Русский язык",
    "📖 Литература",
    "🇬🇧 Английский язык",
    "🇩🇪 Немецкий язык",
    "🇫🇷 Французский язык",
]

SUBJECT_GRADES = {
    "🇷🇺 Русский язык": list(range(1, 12 + 1)),
    "📖 Литература": list(range(5, 12 + 1)),
    "🇬🇧 Английский язык": list(range(2, 11 + 1)),
    "🇩🇪 Немецкий язык": list(range(5, 11 + 1)),
    "🇫🇷 Французский язык": list(range(5, 11 + 1)),
}


async def get_new_generate_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Сгенерировать новый тест", callback_data="new_test"
                )
            ],
        ]
    )


async def get_subject_keyboard() -> InlineKeyboardMarkup:
    keyboard = [
        [InlineKeyboardButton(text=subj, callback_data=f"subject_{subj}")]
        for subj in SUBJECT_AREAS
    ]
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_back_keyboard() -> InlineKeyboardMarkup:
    keyboard = []
    keyboard.append([InlineKeyboardButton(text="Назад", callback_data="back")])
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
        keyboard.append(
            [InlineKeyboardButton(text=section, callback_data=f"grade_block_{section}")]
        )
        row = []
        for i, grade in enumerate(intersection, 1):
            row.append(
                InlineKeyboardButton(
                    text=f"{grade} кл.", callback_data=f"grade_{grade}"
                )
            )
            if i % 2 == 0:
                keyboard.append(row)
                row = []
        if row:
            keyboard.append(row)
    keyboard.append(
        [
            InlineKeyboardButton(
                text="✍🏻 Ввести сложность вручную", callback_data=f"manual_grade"
            )
        ]
    )
    keyboard.append([InlineKeyboardButton(text="Назад", callback_data="back")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


async def get_format_response_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="📜 Открытые вопросы", callback_data="format_open"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✅ Варианты ответов", callback_data="format_choices"
                )
            ],
            [InlineKeyboardButton(text="🔀 Смешанный", callback_data="format_mixed")],
            [InlineKeyboardButton(text="🔠 С пропусками", callback_data="format_pass")],
            [InlineKeyboardButton(text="Назад", callback_data="back")],
        ]
    )


async def get_question_num_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="5 вопросов", callback_data="question_num_5")],
            [InlineKeyboardButton(text="10 вопросов", callback_data="question_num_10")],
            [InlineKeyboardButton(text="Назад", callback_data="back")],
        ]
    )


async def get_answer_question_num_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="2", callback_data="answer_question_num_2"),
                InlineKeyboardButton(text="3", callback_data="answer_question_num_3"),
                InlineKeyboardButton(text="4", callback_data="answer_question_num_4"),
                InlineKeyboardButton(text="Назад", callback_data="back"),
            ],
        ]
    )


async def get_mixed_format_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="~30% открытых", callback_data="mixed_percent_30"
                )
            ],
            [
                InlineKeyboardButton(
                    text="~50% открытых", callback_data="mixed_percent_50"
                )
            ],
            [
                InlineKeyboardButton(
                    text="~70% открытых", callback_data="mixed_percent_70"
                )
            ],
        ]
    )


async def get_file_format_keyboard() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="🔵 Docx", callback_data="file_format_docx")],
            [InlineKeyboardButton(text="🔴 PDF", callback_data="file_format_pdf")],
            [InlineKeyboardButton(text="🟢 Excel", callback_data="file_format_excel")],
        ]
    )
