#!/usr/bin/env python3
"""
Главный файл для запуска Telegram бота ChatBot Becks
"""

import asyncio
import sys
from pathlib import Path

# Добавляем корневую директорию в путь
sys.path.append(str(Path(__file__).parent))

from bot import ChatBot
from config import BOT_TOKEN, LOG_LEVEL, LOG_FILE
from loguru import logger

# Настройка логирования
logger.remove()
logger.add(
    sys.stdout,
    level=LOG_LEVEL,
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)
logger.add(
    LOG_FILE,
    level=LOG_LEVEL,
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}",
    rotation="1 day",
    retention="7 days"
)

async def main():
    """Главная функция запуска бота"""
    try:
        logger.info("Запуск ChatBot Becks...")
        
        # Проверяем токен
        if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
            logger.error("Пожалуйста, установите BOT_TOKEN в config.py или .env файле")
            return
        
        # Создаем и запускаем бота
        bot = ChatBot()
        await bot.start()
        
    except KeyboardInterrupt:
        logger.info("Получен сигнал остановки. Завершение работы...")
    except Exception as e:
        logger.error(f"Ошибка при запуске бота: {e}")
        raise
    finally:
        logger.info("Бот остановлен")

if __name__ == "__main__":
    # Запускаем главную функцию
    asyncio.run(main())
