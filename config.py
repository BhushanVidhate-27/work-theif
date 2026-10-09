import os
from dotenv import load_dotenv

load_dotenv()

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# Models (you can change these)
# Recommended free models (as of now)
WORKER_MODEL = "meta-llama/llama-3.2-3b-instruct"
MANAGER_MODEL = "meta-llama/llama-3.2-3b-instruct"