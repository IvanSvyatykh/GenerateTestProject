import json
from aiohttp import ClientSession
from config import API_URL, DEEP_SEEK_API_KEY


async def deep_seek_request(session: ClientSession, question: str) -> dict:
    headers = {
        "x-rapidapi-key": DEEP_SEEK_API_KEY,
        "x-rapidapi-host": "deepseek-v31.p.rapidapi.com",
        "Content-Type": "application/json",
    }

    payload = {
        "model": "deepseek-v3",
        "messages": [
            {
                "role": "user",
                "content": question,
            }
        ],
    }

    async with session.post(url=API_URL, headers=headers, data=payload) as request:
        response = await request.json()
    return response
