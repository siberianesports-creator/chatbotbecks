"""
Обработчики сообщений для бота
"""

from aiogram import Dispatcher
from .commands import register_command_handlers
from .text import register_text_handlers
from .media import register_media_handlers


def register_handlers(dp: Dispatcher):
    """Регистрация всех обработчиков"""
    register_command_handlers(dp)
    register_text_handlers(dp)
    register_media_handlers(dp)
