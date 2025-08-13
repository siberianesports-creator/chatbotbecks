"""
Вспомогательные функции для бота
"""

from aiogram import Dispatcher
from aiogram.types import Message
from loguru import logger

from config import ADMIN_IDS


async def is_admin(user_id: int) -> bool:
    """Проверка, является ли пользователь администратором"""
    return user_id in ADMIN_IDS


def setup_middlewares(dp: Dispatcher):
    """Настройка middleware для диспетчера"""
    # Здесь можно добавить middleware для логирования, авторизации и т.д.
    logger.info("Middleware настроены")


async def log_message(message: Message):
    """Логирование сообщений"""
    user = message.from_user
    logger.info(
        f"Сообщение от {user.full_name} (ID: {user.id}) "
        f"в чате {message.chat.id}: {message.text or '[медиа]'}"
    )


def format_file_size(size_bytes: int) -> str:
    """Форматирование размера файла"""
    if size_bytes == 0:
        return "0 B"
    
    size_names = ["B", "KB", "MB", "GB", "TB"]
    import math
    i = int(math.floor(math.log(size_bytes, 1024)))
    p = math.pow(1024, i)
    s = round(size_bytes / p, 2)
    return f"{s} {size_names[i]}"


def sanitize_filename(filename: str) -> str:
    """Очистка имени файла от недопустимых символов"""
    import re
    # Удаляем недопустимые символы
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    # Ограничиваем длину
    if len(filename) > 255:
        name, ext = filename.rsplit('.', 1)
        filename = name[:255-len(ext)-1] + '.' + ext
    return filename


def validate_file_extension(filename: str, allowed_extensions: list) -> bool:
    """Проверка расширения файла"""
    import os
    if not filename:
        return False
    
    file_ext = os.path.splitext(filename)[1].lower()
    return file_ext in allowed_extensions


async def send_error_message(message: Message, error: str):
    """Отправка сообщения об ошибке"""
    await message.answer(
        f"❌ <b>Произошла ошибка:</b>\n{error}\n\n"
        "Попробуйте позже или обратитесь к администратору."
    )


def get_user_mention(user) -> str:
    """Получение упоминания пользователя"""
    if user.username:
        return f"@{user.username}"
    else:
        return f"[{user.full_name}](tg://user?id={user.id})"


def truncate_text(text: str, max_length: int = 100) -> str:
    """Обрезка текста до максимальной длины"""
    if len(text) <= max_length:
        return text
    return text[:max_length-3] + "..."
