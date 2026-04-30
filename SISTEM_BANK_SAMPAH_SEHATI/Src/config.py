import os
from dotenv import load_dotenv

# Mengambil data dari file .env yang berada di folder ini
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)

# Data sensitif diambil dari .env
TOKEN = os.getenv("TOKEN")
# Gunakan int() karena ID Telegram biasanya berupa angka
ADMIN_ID = int(os.getenv("ADMIN_ID"))
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Data umum tetap ditulis langsung tidak apa-apa
BOT_NAME = "Sehati Waste Bot"
VERSION = "1.0.0"