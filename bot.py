"""
Основной класс бота ChatBot Becks
"""

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from loguru import logger

from config import BOT_TOKEN, ADMIN_IDS, ENABLE_STATISTICS
from handlers import register_handlers
from database.models import init_database
from utils.helpers import setup_middlewares


class ChatBot:
    """Основной класс бота"""
    
    def __init__(self):
        """Инициализация бота"""
        self.bot = Bot(token=BOT_TOKEN, parse_mode=ParseMode.HTML)
        self.dp = Dispatcher(storage=MemoryStorage())
        self.admin_ids = set(ADMIN_IDS)
        
        # Регистрируем обработчики
        register_handlers(self.dp)
        
        # Настраиваем middleware
        setup_middlewares(self.dp)
        
        # Статистика
        self.stats = {
            "messages_processed": 0,
            "users_active": set(),
            "commands_used": {}
        }
    
    async def start(self):
        """Запуск бота"""
        try:
            logger.info("Инициализация базы данных...")
            await init_database()
            
            logger.info("Запуск бота...")
            await self.dp.start_polling(self.bot)
            
        except Exception as e:
            logger.error(f"Ошибка при запуске бота: {e}")
            raise
    
    async def stop(self):
        """Остановка бота"""
        try:
            logger.info("Остановка бота...")
            await self.bot.session.close()
        except Exception as e:
            logger.error(f"Ошибка при остановке бота: {e}")
    
    def is_admin(self, user_id: int) -> bool:
        """Проверка, является ли пользователь администратором"""
        return user_id in self.admin_ids
    
    async def update_stats(self, message: types.Message, command: str = None):
        """Обновление статистики"""
        if not ENABLE_STATISTICS:
            return
            
        self.stats["messages_processed"] += 1
        self.stats["users_active"].add(message.from_user.id)
        
        if command:
            self.stats["commands_used"][command] = self.stats["commands_used"].get(command, 0) + 1
    
    def get_stats(self) -> dict:
        """Получение статистики"""
        return {
            "messages_processed": self.stats["messages_processed"],
            "users_active": len(self.stats["users_active"]),
            "commands_used": self.stats["commands_used"].copy()
        }
