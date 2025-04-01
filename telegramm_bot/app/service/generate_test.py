from api.rapid_requests import deep_seek_request
from config import GIGA_CHAT_MODEL_NAME, GIGA_CHAT_SECRET_KEY
from gigachat import GigaChat


TEMPLATE = "Сделай тест по {} на тему {} состоящий из {} вопросов, на которые нужно предоставить {}"


async def generate_test(question: str) -> dict:
    giga = GigaChat(
        credentials=GIGA_CHAT_SECRET_KEY,
        model=GIGA_CHAT_MODEL_NAME,
        verify_ssl_certs=False,
    )
    res = await giga.achat(question)
    return res
