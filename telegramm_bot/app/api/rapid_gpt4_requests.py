from config import GPT4_RAPIDAPI_KEYS, GPT4_API_URL
import logging
from aiohttp import ClientSession


async def gpt4_request(session: ClientSession, user_prompt: str) -> dict:
    payload = {
        "messages": [
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        "web_access": True
    }

    for api_key in GPT4_RAPIDAPI_KEYS:
        headers = {
            "x-rapidapi-key": api_key.strip(),
            "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        try:
            async with session.post(url=GPT4_API_URL, headers=headers, json=payload) as request:
                if request.status == 200:
                    response = await request.json()
                    return response
                elif request.status == 429:
                    logging.warning(f"Израсходован ключ: {api_key}, пробую другой")
                    continue
                else:
                    logging.error(f"Error: {request.status} с ключем: {api_key}")
                    continue
        except Exception as e:
            logging.exception(f"Error: key: {api_key}: {e}")
            continue

    logging.critical("All API keys are exhausted or failed.")
    return {"error": "All API keys failed or rate limited."}


def create_user_prompt(data: dict) -> str:
    subject_area = data.get("subject_area")
    subject = data.get("subject")
    theme = data.get("theme")
    complexity = data.get("complexity")
    format_response = data.get("format_response")
    answer_num = data.get("answer_num")
    question_num = data.get("question_num")
    mixed_percent = data.get("mixed_percent")

    prompt = (
        f"Создай тест из {question_num} вопросов по теме '{theme}' "
        f"в предмете '{subject}' (область: {subject_area}). "
        f"Сложность: {complexity.replace('🔹', '').replace('🔸', '').replace('🔺', '').strip()}. "
    )

    if format_response == "📜 Открытые вопросы":
        prompt += "Формат: только открытые вопросы. "
    elif format_response == "✅ Варианты ответов":
        prompt += f"Формат: только с вариантами ответов. У каждого вопроса должно быть {answer_num} вариантов. "
    elif format_response == "🔀 Смешанный":
        prompt += f"Формат: смешанный. {mixed_percent}% вопросов с вариантами, {100 - int(mixed_percent)}% — открытые. "
        prompt += f"У вопросов с вариантами должно быть {answer_num} вариантов. "

    prompt += (
        "Ответ должен быть в формате JSON, без лишнего текста, знаков оформления и прочего. Строго только JSON. "
        "Каждый вопрос должен содержать 'question', 'answers' и 'correct_answer'. Структура должна быть такая:"
        """{
          "questions": [
            {
              "question":
              "answers": [
                
              ],
              "correct_answer":
            },"""
        "ВОПРОСЫ И ОТВЕТЫ НА РУССКОМ ЯЗЫКЕ"
    )

    return prompt
