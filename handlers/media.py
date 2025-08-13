"""
Обработчики медиа-файлов
"""

from aiogram import Dispatcher, types, F
from aiogram.fsm.context import FSMContext
from loguru import logger
import os

from database.models import update_user_activity
from config import UPLOAD_PATH, ALLOWED_EXTENSIONS, MAX_FILE_SIZE
from utils.ai_services import ai_services


async def handle_photo(message: types.Message, state: FSMContext):
    """Обработчик фотографий"""
    try:
        user_id = message.from_user.id
        await update_user_activity(user_id)
        
        # Получаем информацию о фото
        photo = message.photo[-1]  # Берем самое большое фото
        file_id = photo.file_id
        file_size = photo.file_size
        
        logger.info(f"Получено фото от {message.from_user.full_name} (ID: {user_id}), размер: {file_size} байт")
        
        # Проверяем размер файла
        if file_size and file_size > MAX_FILE_SIZE * 1024 * 1024:
            await message.answer(f"⚠️ Файл слишком большой. Максимальный размер: {MAX_FILE_SIZE} MB")
            return
        
        # Анализируем изображение с помощью AI
        try:
            # Получаем файл изображения
            file = await message.bot.get_file(file_id)
            file_data = await message.bot.download_file(file.file_path)
            
            # Анализируем с помощью Gemini
            analysis = await ai_services.analyze_image_with_gemini(file_data.read())
            
            if analysis:
                response = f"""
📸 <b>Получено фото!</b>

<b>Информация:</b>
• Размер: {file_size or 'Неизвестно'} байт
• ID файла: {file_id}
• Отправитель: {message.from_user.full_name}

🤖 <b>AI анализ:</b>
{analysis}

<b>Что я могу сделать:</b>
• Сохранить фото
• Обработать изображение
• Отправить обратно

Спасибо за фото! 😊
                """
            else:
                response = f"""
📸 <b>Получено фото!</b>

<b>Информация:</b>
• Размер: {file_size or 'Неизвестно'} байт
• ID файла: {file_id}
• Отправитель: {message.from_user.full_name}

<b>Что я могу сделать:</b>
• Сохранить фото
• Обработать изображение
• Отправить обратно

Спасибо за фото! 😊
                """
        except Exception as e:
            logger.error(f"Error analyzing image: {e}")
            response = f"""
📸 <b>Получено фото!</b>

<b>Информация:</b>
• Размер: {file_size or 'Неизвестно'} байт
• ID файла: {file_id}
• Отправитель: {message.from_user.full_name}

<b>Что я могу сделать:</b>
• Сохранить фото
• Обработать изображение
• Отправить обратно

Спасибо за фото! 😊
            """
        
        await message.answer(response)
        
    except Exception as e:
        logger.error(f"Ошибка при обработке фото: {e}")
        await message.answer("Произошла ошибка при обработке фото.")


async def handle_video(message: types.Message, state: FSMContext):
    """Обработчик видео"""
    try:
        user_id = message.from_user.id
        await update_user_activity(user_id)
        
        video = message.video
        file_id = video.file_id
        file_size = video.file_size
        duration = video.duration
        width = video.width
        height = video.height
        
        logger.info(f"Получено видео от {message.from_user.full_name} (ID: {user_id})")
        
        # Проверяем размер файла
        if file_size and file_size > MAX_FILE_SIZE * 1024 * 1024:
            await message.answer(f"⚠️ Файл слишком большой. Максимальный размер: {MAX_FILE_SIZE} MB")
            return
        
        response = f"""
🎥 <b>Получено видео!</b>

<b>Информация:</b>
• Размер: {file_size or 'Неизвестно'} байт
• Длительность: {duration or 'Неизвестно'} секунд
• Разрешение: {width}x{height}
• ID файла: {file_id}

<b>Что я могу сделать:</b>
• Сохранить видео
• Извлечь кадры
• Создать превью

Отличное видео! 🎬
        """
        
        await message.answer(response)
        
    except Exception as e:
        logger.error(f"Ошибка при обработке видео: {e}")
        await message.answer("Произошла ошибка при обработке видео.")


async def handle_document(message: types.Message, state: FSMContext):
    """Обработчик документов"""
    try:
        user_id = message.from_user.id
        await update_user_activity(user_id)
        
        document = message.document
        file_name = document.file_name
        file_size = document.file_size
        mime_type = document.mime_type
        
        logger.info(f"Получен документ от {message.from_user.full_name} (ID: {user_id}): {file_name}")
        
        # Проверяем расширение файла
        if file_name:
            file_ext = os.path.splitext(file_name)[1].lower()
            if file_ext not in ALLOWED_EXTENSIONS:
                await message.answer(f"⚠️ Тип файла не поддерживается. Разрешенные форматы: {', '.join(ALLOWED_EXTENSIONS)}")
                return
        
        # Проверяем размер файла
        if file_size and file_size > MAX_FILE_SIZE * 1024 * 1024:
            await message.answer(f"⚠️ Файл слишком большой. Максимальный размер: {MAX_FILE_SIZE} MB")
            return
        
        response = f"""
📄 <b>Получен документ!</b>

<b>Информация:</b>
• Название: {file_name or 'Неизвестно'}
• Размер: {file_size or 'Неизвестно'} байт
• Тип: {mime_type or 'Неизвестно'}

<b>Что я могу сделать:</b>
• Сохранить документ
• Прочитать содержимое (если текстовый)
• Создать резервную копию

Документ получен! 📋
        """
        
        await message.answer(response)
        
    except Exception as e:
        logger.error(f"Ошибка при обработке документа: {e}")
        await message.answer("Произошла ошибка при обработке документа.")


async def handle_voice(message: types.Message, state: FSMContext):
    """Обработчик голосовых сообщений"""
    try:
        user_id = message.from_user.id
        await update_user_activity(user_id)
        
        voice = message.voice
        duration = voice.duration
        file_size = voice.file_size
        
        logger.info(f"Получено голосовое сообщение от {message.from_user.full_name} (ID: {user_id})")
        
        response = f"""
🎤 <b>Получено голосовое сообщение!</b>

<b>Информация:</b>
• Длительность: {duration} секунд
• Размер: {file_size or 'Неизвестно'} байт

<b>Что я могу сделать:</b>
• Сохранить аудио
• Конвертировать в текст (в будущем)
• Создать транскрипцию

Голосовое сообщение получено! 🎵
        """
        
        await message.answer(response)
        
    except Exception as e:
        logger.error(f"Ошибка при обработке голосового сообщения: {e}")
        await message.answer("Произошла ошибка при обработке голосового сообщения.")


def register_media_handlers(dp: Dispatcher):
    """Регистрация обработчиков медиа-файлов"""
    dp.message.register(handle_photo, F.photo)
    dp.message.register(handle_video, F.video)
    dp.message.register(handle_document, F.document)
    dp.message.register(handle_voice, F.voice)
