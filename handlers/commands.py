"""
Обработчики команд бота
"""

from aiogram import Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from loguru import logger

from keyboards.reply import get_main_keyboard, get_admin_keyboard
from database.models import User, get_user_by_id, create_user
from utils.helpers import is_admin


async def cmd_start(message: types.Message, state: FSMContext):
    """Обработчик команды /start"""
    try:
        user_id = message.from_user.id
        user_name = message.from_user.full_name
        username = message.from_user.username
        
        # Проверяем, есть ли пользователь в базе
        user = await get_user_by_id(user_id)
        if not user:
            # Создаем нового пользователя
            await create_user(user_id, user_name, username)
            logger.info(f"Новый пользователь: {user_name} (ID: {user_id})")
        
        welcome_text = f"""
🎉 <b>Добро пожаловать в ChatBot Becks!</b>

Привет, {user_name}! Я современный Telegram бот с множеством возможностей.

<b>Доступные команды:</b>
/start - Начать работу с ботом
/help - Показать справку
/profile - Ваш профиль
/settings - Настройки

<b>Возможности:</b>
• Обработка текстовых сообщений
• Поддержка медиа-файлов
• Инлайн-кнопки и клавиатуры
• Система команд администратора

Выберите действие или напишите мне сообщение!
        """
        
        await message.answer(
            welcome_text,
            reply_markup=get_main_keyboard()
        )
        
        # Очищаем состояние
        await state.clear()
        
    except Exception as e:
        logger.error(f"Ошибка в команде /start: {e}")
        await message.answer("Произошла ошибка. Попробуйте позже.")


async def cmd_help(message: types.Message):
    """Обработчик команды /help"""
    help_text = """
📚 <b>Справка по ChatBot Becks</b>

<b>Основные команды:</b>
/start - Начать работу с ботом
/help - Показать эту справку
/profile - Ваш профиль
/settings - Настройки

<b>Дополнительные команды:</b>
/feedback - Отправить отзыв
/contact - Связаться с поддержкой

<b>Для администраторов:</b>
/admin - Панель администратора
/stats - Статистика бота
/broadcast - Отправить сообщение всем пользователям

<b>Как использовать:</b>
1. Отправьте текстовое сообщение - бот ответит
2. Отправьте фото/видео - бот обработает медиа
3. Используйте кнопки для навигации
4. Обратитесь к администратору при проблемах

<b>Поддержка:</b>
Если у вас есть вопросы, используйте команду /contact
        """
    
    await message.answer(help_text)


async def cmd_profile(message: types.Message):
    """Обработчик команды /profile"""
    try:
        user_id = message.from_user.id
        user = await get_user_by_id(user_id)
        
        if user:
            profile_text = f"""
👤 <b>Ваш профиль</b>

<b>Имя:</b> {user.full_name}
<b>Username:</b> @{user.username or 'Не указан'}
<b>ID:</b> {user.user_id}
<b>Дата регистрации:</b> {user.created_at.strftime('%d.%m.%Y %H:%M')}
<b>Сообщений отправлено:</b> {user.messages_count}
<b>Последняя активность:</b> {user.last_activity.strftime('%d.%m.%Y %H:%M')}
            """
        else:
            profile_text = "Профиль не найден. Используйте /start для регистрации."
        
        await message.answer(profile_text)
        
    except Exception as e:
        logger.error(f"Ошибка в команде /profile: {e}")
        await message.answer("Произошла ошибка при получении профиля.")


async def cmd_admin(message: types.Message):
    """Обработчик команды /admin"""
    if not await is_admin(message.from_user.id):
        await message.answer("⛔ У вас нет доступа к панели администратора.")
        return
    
    admin_text = """
🔧 <b>Панель администратора</b>

Выберите действие:

📊 <b>Статистика:</b>
/stats - Общая статистика бота
/users - Список пользователей

📢 <b>Рассылка:</b>
/broadcast - Отправить сообщение всем
/broadcast_photo - Отправить фото всем

⚙️ <b>Управление:</b>
/backup - Создать резервную копию
/restart - Перезапустить бота
        """
    
    await message.answer(
        admin_text,
        reply_markup=get_admin_keyboard()
    )


async def cmd_stats(message: types.Message):
    """Обработчик команды /stats"""
    if not await is_admin(message.from_user.id):
        await message.answer("⛔ У вас нет доступа к статистике.")
        return
    
    # Здесь будет логика получения статистики
    stats_text = """
📊 <b>Статистика бота</b>

<b>Общая информация:</b>
• Всего пользователей: 0
• Активных сегодня: 0
• Сообщений обработано: 0

<b>Популярные команды:</b>
• /start: 0 использований
• /help: 0 использований

<b>Система:</b>
• Время работы: 0 минут
• Статус: Активен
        """
    
    await message.answer(stats_text)


def register_command_handlers(dp: Dispatcher):
    """Регистрация обработчиков команд"""
    dp.message.register(cmd_start, Command("start"))
    dp.message.register(cmd_help, Command("help"))
    dp.message.register(cmd_profile, Command("profile"))
    dp.message.register(cmd_admin, Command("admin"))
    dp.message.register(cmd_stats, Command("stats"))
