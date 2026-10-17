import os
from dotenv import load_dotenv


load_dotenv()
INTERVAL = 1800
TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("Не найден токен!")
