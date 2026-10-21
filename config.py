import os
from dotenv import load_dotenv


load_dotenv()
INTERVAL = 1800
TOKEN = os.getenv("TOKEN")
ADMIN = os.getenv("ADMIN")

if not TOKEN:
    raise RuntimeError("Не найден токен!")
if not ADMIN:
    raise RuntimeError("Не найден админ!")
