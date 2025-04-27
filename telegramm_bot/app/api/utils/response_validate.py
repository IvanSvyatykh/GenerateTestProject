import json


def validate_json(test_json: dict, format_response: str) -> bool:
    if not isinstance(test_json, dict) or "questions" not in test_json:
        return False

    for question in test_json.get("questions", []):
        if "question" not in question:
            return False

        if format_response == "📜 Открытые вопросы":
            if "answers" in question or "correct_answer" not in question:
                return False
        elif format_response == "✅ Варианты ответов" or format_response =="🔠 С пропусками":
            if "answers" not in question or "correct_answer" not in question:
                return False
        elif format_response == "🔀 Смешанный":
            if "type" not in question or "correct_answer" not in question:
                return False
            if question["type"] == "choice":
                if "answers" not in question:
                    return False
            elif question["type"] == "open" and "answers" in question:
                return False
        else:
            return False
    return True
