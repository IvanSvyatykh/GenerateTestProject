import os
from dotenv import load_dotenv

load_dotenv()
# Bot envs
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEB_HOOK_URL = os.getenv("WEB_HOOK_URL")
WEB_HOOK_PATH = os.getenv("WEB_HOOK_PATH")
WEB_SERVER_HOST = os.getenv("WEB_SERVER_HOST")
# API env
DEEP_SEEK_API_KEY = os.getenv("DEEP_SEEK_API_KEY")
API_URL = os.getenv("API_URL")
# Rapid Api
GPT4_RAPIDAPI_KEYS = os.getenv("GPT4_RAPIDAPI_KEYS", "").split(",")
GPT4_API_URL = os.getenv("GPT4_API_URL")
# Giga chat
GIGA_CHAT_SECRET_KEY = os.getenv("GIGA_CHAT_SECRET_KEY")
GIGA_CHAT_MODEL_NAME = os.getenv("GIGA_CHAT_MODEL_NAME")
# Postgres
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_DOMAIN = os.getenv("POSTGRES_DOMAIN")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")
POSTGRES_DB_NAME = os.getenv("POSTGRES_DB_NAME")
