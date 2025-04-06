GREETING_MESS = ("👋 *Привет!* 👋\n🤖 Я бот, который может *генерировать тесты* по различным предметам и темам.\n\n"
                 "📚 *Выберите предметную область:*")

CHOOSE_SUBJECT_AREA = "🧠 Для генерации нового теста:\n📚 *Выберите предметную область:*"

MANUAL_AREA = ("✍🏻 *Введите предментую область*\n"
               "Например:\n"
               "- 🎬 Кинематограф\n"
               "- 🏀 Баскетбол")

MANUAL_SUBJECT = ("📚 Предметная область: {subject_area}\n\n"
                  "✍🏻 *Введите предмент*\n"
                  "Например:\n"
                  "- 💃🏼 Естествознание\n"
                  "- 🌏 Мировая экономика")

CHOOSE_SUBJECT = ("📚 Предметная область: {subject_area}\n\n"
                  "📘 *Выберите предмет*, по которому вы хотите сгенерировать тест:")

CHOOSE_THEME = (
    "📚 Предметная область: {subject_area}\n"
    "📘 Предмет: {subject}\n\n"
    "✍🏻 *Введите тему теста*\n"
    "Например:\n"
    "- 🐍 рептилии\n"
    "- ⚔️ столетняя война"
)

CHOOSE_COMPLEXITY = (
    "📚 Предметная область: {subject_area}\n"
    "📘 Предмет: {subject}\n"
    "🔎 Тема: {theme}\n\n"
    "🎯 *Выберите сложность теста:*"
)

CHOOSE_FORMAT_RESPONSE = (
    "📚 Предметная область: {subject_area}\n"
    "📘 Предмет: {subject}\n"
    "🔎 Тема: {theme}\n"
    "🎯 Сложность: {complexity}\n\n"
    "🗂️ *Выберите формат ответов:*"
)

CHOOSE_ANSWER_NUM = (
    "📚 Предметная область: {subject_area}\n"
    "📘 Предмет: {subject}\n"
    "🔎 Тема: {theme}\n"
    "🎯 Сложность: {complexity}\n"
    "🗂️ Формат ответов: {format_response}\n\n"
    "🔠 *Выберите количество вариантов ответа:*"
)

CHOOSE_QUESTION_NUM = (
    "📚 Предметная область: {subject_area}\n"
    "📘 Предмет: {subject}\n"
    "🔎 Тема: {theme}\n"
    "🎯 Сложность: {complexity}\n"
    "🗂️ Формат ответов: {format_response}\n\n"
    "🔢 *Выберите количество вопросов в тесте:*"
)

CHOOSE_QUESTION_NUM_WITH_ANSWER_NUM = (
    "📚 Предметная область: {subject_area}\n"
    "📘 Предмет: {subject}\n"
    "🔎 Тема: {theme}\n"
    "🎯 Сложность: {complexity}\n"
    "🗂️ Формат ответов: {format_response}\n"
    "☑️ Количетсво вариантов ответа:  {answer_num}\n\n"
    "🔢 *Выберите количество вопросов в тесте:*"
)

CHOOSE_QUESTION_NUM_WITH_ANSWER_NUM_AND_PERCENT = (
    "📚 Предметная область: {subject_area}\n"
    "📘 Предмет: {subject}\n"
    "🔎 Тема: {theme}\n"
    "🎯 Сложность: {complexity}\n"
    "🗂️ Формат ответов: {format_response}\n"
    "☑️ Количетсво вариантов ответа:  {answer_num}\n"
    "📊 Процент открытых вопросов:  {mixed_percent}%\n\n"
    "🔢 *Выберите количество вопросов в тесте:*"
)

CHOOSE_PERCENT_FORMAT_RESPONSE = (
    "📚 Предметная область: {subject_area}\n"
    "📘 Предмет: {subject}\n"
    "🔎 Тема: {theme}\n"
    "🎯 Сложность: {complexity}\n"
    "🗂️ Формат ответов: {format_response}\n"
    "☑️ Количетсво вариантов ответа:  {answer_num}\n\n"
    "📊 *Выберите % открытых вопросов:*\n_(остальные будут с вариантами ответов)_"
)

FINISHED_TEST = (
    "📚 Предметная область: {subject_area}\n"
    "📘 Предмет: {subject}\n"
    "🔎 Тема: {theme}\n"
    "🎯 Сложность: {complexity}\n"
    "🗂️ Формат ответов: {format_response}\n"
    "🔢 Количество вопросов:  {question_num}\n\n"
    "✅ *Ваш тест готов!*\n"
    "*Выберите формат файла:*"
)

FINISHED_TEST_WITH_ANSWER_NUM = (
    "📚 Предметная область: {subject_area}\n"
    "📘 Предмет: {subject}\n"
    "🔎 Тема: {theme}\n"
    "🎯 Сложность: {complexity}\n"
    "🗂️ Формат ответов: {format_response}\n"
    "☑️ Количетсво вариантов ответа:  {answer_num}\n"
    "🔢 Количество вопросов:  {question_num}\n\n"
    "✅ *Ваш тест готов!*\n"
    "*Выберите формат файла:*"
)

FINISHED_TEST_WITH_ANSWER_NUM_AND_PERCENT = (
    "📚 Предметная область: {subject_area}\n"
    "📘 Предмет: {subject}\n"
    "🔎 Тема: {theme}\n"
    "🎯 Сложность: {complexity}\n"
    "🗂️ Формат ответов: {format_response}\n"
    "☑️ Количетсво вариантов ответа:  {answer_num}\n"
    "📊 Процент открытых вопросов:  {mixed_percent}%\n"
    "🔢 Количество вопросов:  {question_num}\n\n"
    "✅ *Ваш тест готов!*\n"
    "*Выберите формат файла:*"
)
