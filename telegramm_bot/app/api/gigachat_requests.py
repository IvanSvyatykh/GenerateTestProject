import os
import json
import logging
import uuid
import aiohttp
import asyncio
import ssl
from datetime import datetime, timedelta
from dotenv import load_dotenv
from api.utils.response_validate import validate_json

load_dotenv()

GIGACHAT_AUTH_KEY = os.getenv("GIGACHAT_AUTH_KEY")
GIGACHAT_SCOPE = "GIGACHAT_API_PERS"
GIGACHAT_OAUTH_URL = "https://ngw.devices.sberbank.ru:9443/api/v2/oauth"
GIGACHAT_CHAT_URL = "https://gigachat.devices.sberbank.ru/api/v1/chat/completions"

# кэш токена
token_cache = {
    "access_token": None,
    "expires_at": datetime.min
}


async def get_access_token():
    now = datetime.utcnow()

    if token_cache["access_token"] and token_cache["expires_at"] > now:
        return token_cache["access_token"]

    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Accept": "application/json",
        "RqUID": str(uuid.uuid4()),
        "Authorization": f"Basic {GIGACHAT_AUTH_KEY}"
    }
    data = {
        "scope": GIGACHAT_SCOPE
    }

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession() as session:
        async with session.post(
            GIGACHAT_OAUTH_URL, headers=headers, data=data, ssl=ssl_context
        ) as resp:
            result = await resp.json()
            access_token = result.get("access_token")
            expires_in = result.get("expires_in", 1800)

            if access_token:
                token_cache["access_token"] = access_token
                token_cache["expires_at"] = now + timedelta(seconds=expires_in - 10)
                return access_token
            else:
                logging.error(f"Ошибка получения токена: {result}")
                return None


async def gigachat_request(user_prompt: str, format_response: str) -> dict:
    token = await get_access_token()
    if not token:
        return {"error": "Не удалось получить токен"}

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
        "Accept": "application/json"
    }

    payload = {
        "model": "GigaChat-Pro",
        "messages": [{"role": "user", "content": user_prompt}],
        "temperature": 0.7
    }

    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    async with aiohttp.ClientSession() as session:
        async with session.post(GIGACHAT_CHAT_URL, headers=headers, json=payload, ssl=ssl_context) as resp:
            try:
                result = await resp.json()
                content = result["choices"][0]["message"]["content"]
                raw_json = content.strip("```json\\n").strip("\\n```")

                test_json = json.loads(raw_json)
                validation_result = validate_json(test_json, format_response)
                if not validation_result:
                    raise ValueError("Невалидный JSON")

                return test_json

            except Exception as e:
                logging.exception(f"Ошибка разбора ответа: {e}")
                return {"error": str(e)}

