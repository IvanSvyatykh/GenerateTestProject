import asyncio

from handlers.utils.shared import loading_tasks


async def animate_loading(bot, chat_id, message_id, key):
    dots = [".", "..", "..."]
    i = 0
    try:
        while True:
            text = f"⏳ Генерирую тест{dots[i % 3]}"
            await bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)
            i += 1
            await asyncio.sleep(1)
    except asyncio.CancelledError:
        pass
    finally:
        loading_tasks.pop(key, None)
