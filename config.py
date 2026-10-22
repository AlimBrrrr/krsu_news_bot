import os
from dotenv import load_dotenv


load_dotenv()
INTERVAL = 1800
TOKEN = os.getenv("TOKEN")
ADMIN = os.getenv("ADMIN")

if not TOKEN:
    raise RuntimeError("The token has not found!")
if not ADMIN:
    raise RuntimeError("The admin has not found!")
