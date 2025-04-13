import asyncio
import logging
import json
from aiohttp import ClientSession
from config import GPT4_RAPIDAPI_KEYS, GPT4_API_URL
from api.utils.response_validate import validate_json


async def gpt4_request(user_prompt: str, format_response: str) -> dict:
    payload = {
        "messages": [
            {
                "role": "user",
                "content": user_prompt
            }
        ],
        "web_access": False
    }

    timeout = 100
    for api_key in GPT4_RAPIDAPI_KEYS:
        headers = {
            "x-rapidapi-key": api_key.strip(),
            "x-rapidapi-host": "chatgpt-42.p.rapidapi.com",
            "Content-Type": "application/json"
        }

        try:
            async with ClientSession() as session:
                try:
                    async with session.post(url=GPT4_API_URL, headers=headers, json=payload) as request:
                        response = await request.json()

                    if request.status == 200:
                        raw_json = response.get("result", "").strip('```json\n').strip('\n```')

                        try:
                            test_json = json.loads(raw_json)
                            print(test_json)

                            validation_result = validate_json(test_json, format_response)
                            if not validation_result:
                                raise ValueError(f"Некорректный JSON: {validation_result['error']}")

                            return test_json

                        except (json.JSONDecodeError, ValueError) as e:
                            print(response.get("result", ""))
                            logging.warning(f"Ошибка в структуре JSON: {e}, пробую снова.")
                            break

                except asyncio.TimeoutError:
                    print(response.get("result", ""))
                    logging.warning(f"Тайм-аут при запросе с ключом {api_key}, пробую снова.")
                    continue

                if request.status == 429:
                    print(response.get("result", ""))
                    logging.warning(f"Израсходован ключ: {api_key}, пробую другой")
                    continue
                elif request.status == 504:
                    print(response.get("result", ""))
                    logging.warning(f"Time out с ключом: {api_key}, пробую другой")
                    continue
                else:
                    print(response.get("result", ""))
                    logging.error(f"Error: {request.status} с ключом: {api_key}")
                    continue

        except Exception as e:
            print(response.get("result", ""))
            logging.exception(f"Ошибка при запросе с ключом {api_key}: {e}")
            continue

    logging.info("Попытки с этим ключом не удались, пробую следующий.")
    await asyncio.sleep(1)

    logging.critical("Все ключи API не работают или достигнут лимит.")
    return {"error": "Все ключи API не работают или достигнут лимит."}
