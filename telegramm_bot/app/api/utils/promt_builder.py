def create_user_prompt(data: dict) -> str:
    subject = data.get("subject")
    theme = data.get("theme")
    complexity = data.get("complexity")
    format_response = data.get("format_response")
    answer_num = data.get("answer_num")
    question_num = data.get("question_num")
    mixed_percent = data.get("mixed_percent")

    if format_response == "📜 Открытые вопросы":
        format_description = (
            "Ответ должен быть в JSON формате со списком вопросов. "
            "Каждый вопрос содержит: 'question' (текст вопроса), 'correct_answer' (текст ответа)."
            "Структура должна быть такая:"
            """{
                      "questions": [
                        {
                          "question":
                          "correct_answer":
                        },"""
        )
    elif format_response == "✅ Варианты ответов":
        format_description = (
            "Ответ должен быть в JSON формате со списком вопросов. "
            "Каждый вопрос содержит: 'question' (текст вопроса), 'answers' (список вариантов ответа), "
            "'correct_answer' (индекс правильного ответа). Структура должна быть такая:"
            """{
                      "questions": [
                        {
                          "question":
                          "answers": [

                          ],
                          "correct_answer":
                        },"""
        )
    elif format_response == "🔀 Смешанный":
        format_description = (
            "Ответ должен быть в JSON формате со списком вопросов. "
            "Часть из них с открытым ответом, часть с выбором. "
            "Каждый вопрос обязательно должен содержать 'question'. "
            "Если это вопрос с выбором — также 'answers' и 'correct_answer'. "
            "Если открытый — только 'correct_answer'. Структура должна быть такая для вопросов с выбором ответа:"
            """{
                      "questions": [
                        {
                          "type": "choice"
                          "question":
                          "answers": [

                          ],
                          "correct_answer":
                        },"""
            "И структура должна быть такая для вопросов с открытым ответом:"
            """{
                      "questions": [
                        {
                          "type": "open"
                          "question":
                          "correct_answer":
                        },"""
        )
    else:
        format_description = "Неизвестный формат."

    lang_instruction = (
        f"ВОПРОСЫ И ОТВЕТЫ НА {subject.upper()}"
        if subject in ["🇬🇧 Английский язык", "🇩🇪 Немецкий язык", "🇫🇷 Французский язык"]
        else "ВОПРОСЫ И ОТВЕТЫ НА РУССКОМ ЯЗЫКЕ"
    )

    prompt = (
        f"Создай тест из {question_num} вопросов по теме '{theme}' для предмета '{subject}', "
        f"уровень сложности: {complexity.replace('🔹', '').replace('🔸', '').replace('🔺', '').strip()}. "
        f"{f'У каждого вопроса должно быть {answer_num} вариантов ответа. ' if answer_num else ''}"
        f"{f'Примерно {mixed_percent}% вопросов должно быть смешанными. ' if mixed_percent else ''}"
        f"{format_description}\n"
        f"{lang_instruction}.\n"
        f"ВЕРНИ ТОЛЬКО JSON, БЕЗ ОБЪЯСНЕНИЙ, ПОЯСНЕНИЙ И ПРОЧЕГО."
    )

    return prompt
