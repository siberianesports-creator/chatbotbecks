"""
Обработчики текстовых сообщений
"""

from aiogram import Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from loguru import logger

from database.models import update_user_activity, increment_message_count
from utils.helpers import is_admin


async def handle_text_message(message: types.Message, state: FSMContext):
    """Обработчик текстовых сообщений"""
    try:
        user_id = message.from_user.id
        text = message.text
        
        # Обновляем активность пользователя
        await update_user_activity(user_id)
        await increment_message_count(user_id)
        
        # Логируем сообщение
        logger.info(f"Сообщение от {message.from_user.full_name} (ID: {user_id}): {text}")
        
        # Простая логика ответа
        if "привет" in text.lower():
            response = f"Привет, {message.from_user.first_name}! 👋"
        elif "как дела" in text.lower():
            response = "Спасибо, у меня все отлично! А у вас как дела? 😊"
        elif "спасибо" in text.lower():
            response = "Пожалуйста! Рад быть полезным! 🙏"
        elif "пока" in text.lower() or "до свидания" in text.lower():
            response = "До свидания! Буду ждать нашего следующего разговора! 👋"
        elif "помощь" in text.lower() or "help" in text.lower():
            response = """
📚 <b>Как я могу помочь?</b>

<b>Основные команды:</b>
/start - Начать работу
/help - Подробная справка
/profile - Ваш профиль

<b>Что я умею:</b>
• Отвечать на сообщения
• Обрабатывать медиа-файлы
• Показывать статистику
• Помогать администраторам

Просто напишите мне что-нибудь, и я постараюсь помочь!
            """
        else:
            response = f"""
💬 <b>Получено ваше сообщение:</b>
"{text}"

Я обработал ваше сообщение и готов помочь! 

<b>Что вы можете сделать:</b>
• Задать вопрос
• Отправить команду /help для справки
• Отправить медиа-файл
• Использовать кнопки меню

Пишите, что угодно! 😊
            """
        
        await message.answer(response)
        
    except Exception as e:
        logger.error(f"Ошибка при обработке текстового сообщения: {e}")
        await message.answer("Произошла ошибка при обработке сообщения. Попробуйте позже.")


async def handle_unknown_message(message: types.Message):
    """Обработчик неизвестных типов сообщений"""
    await message.answer(
        "🤔 Я получил сообщение, но не знаю, как его обработать.\n"
        "Попробуйте отправить текстовое сообщение или используйте команду /help"
    )


def register_text_handlers(dp: Dispatcher):
    """Регистрация обработчиков текстовых сообщений"""
    dp.message.register(handle_text_message, F.text)
    dp.message.register(handle_unknown_message)
