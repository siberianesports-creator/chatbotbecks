import os
from dotenv import load_dotenv

# Загружаем переменные окружения из .env файла
load_dotenv()

# Токен бота (получите у @BotFather)
BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# ID администраторов (замените на реальные ID)
ADMIN_IDS = [
    int(id.strip()) for id in os.getenv("ADMIN_IDS", "123456789").split(",")
]

# Настройки базы данных
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///bot.db")

# Настройки логирования
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
LOG_FILE = os.getenv("LOG_FILE", "bot.log")

# Настройки бота
BOT_NAME = "ChatBot Becks"
BOT_USERNAME = os.getenv("BOT_USERNAME", "your_bot_username")

# Настройки веб-хуков (для продакшена)
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "")
WEBHOOK_PATH = os.getenv("WEBHOOK_PATH", "/webhook")

# Настройки прокси (если нужно)
PROXY_URL = os.getenv("PROXY_URL", "")

# Настройки Redis (для кэширования)
REDIS_URL = os.getenv("REDIS_URL", "")

# Настройки файлов
UPLOAD_PATH = os.getenv("UPLOAD_PATH", "uploads")
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", "50"))  # MB

# Настройки безопасности
ALLOWED_EXTENSIONS = [".jpg", ".jpeg", ".png", ".gif", ".mp4", ".pdf", ".doc", ".docx"]
MAX_MESSAGE_LENGTH = int(os.getenv("MAX_MESSAGE_LENGTH", "4096"))

# Настройки локализации
DEFAULT_LANGUAGE = os.getenv("DEFAULT_LANGUAGE", "ru")

# Настройки уведомлений
ENABLE_NOTIFICATIONS = os.getenv("ENABLE_NOTIFICATIONS", "true").lower() == "true"
NOTIFICATION_CHAT_ID = os.getenv("NOTIFICATION_CHAT_ID", "")

# Настройки статистики
ENABLE_STATISTICS = os.getenv("ENABLE_STATISTICS", "true").lower() == "true"
