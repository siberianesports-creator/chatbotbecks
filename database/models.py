"""
Модели базы данных
"""

from sqlalchemy import create_engine, Column, Integer, String, DateTime, Boolean, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import func
from datetime import datetime
from loguru import logger

from config import DATABASE_URL

# Создаем базовый класс для моделей
Base = declarative_base()

# Создаем движок базы данных
engine = create_engine(DATABASE_URL, echo=False)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class User(Base):
    """Модель пользователя"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, unique=True, index=True, nullable=False)
    username = Column(String(255), nullable=True)
    full_name = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    messages_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=func.now())
    last_activity = Column(DateTime, default=func.now())
    language_code = Column(String(10), default="ru")
    settings = Column(Text, nullable=True)  # JSON строка с настройками


class Message(Base):
    """Модель сообщения"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    message_id = Column(Integer, nullable=False)
    chat_id = Column(Integer, nullable=False)
    message_type = Column(String(50), nullable=False)  # text, photo, video, etc.
    content = Column(Text, nullable=True)
    file_id = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=func.now())


class Statistics(Base):
    """Модель статистики"""
    __tablename__ = "statistics"
    
    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, default=func.now())
    total_users = Column(Integer, default=0)
    active_users = Column(Integer, default=0)
    total_messages = Column(Integer, default=0)
    commands_used = Column(Text, nullable=True)  # JSON строка


async def init_database():
    """Инициализация базы данных"""
    try:
        # Создаем все таблицы
        Base.metadata.create_all(bind=engine)
        logger.info("База данных инициализирована успешно")
    except Exception as e:
        logger.error(f"Ошибка при инициализации базы данных: {e}")
        raise


def get_db():
    """Получение сессии базы данных"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_user_by_id(user_id: int) -> User:
    """Получение пользователя по ID"""
    db = SessionLocal()
    try:
        return db.query(User).filter(User.user_id == user_id).first()
    finally:
        db.close()


async def create_user(user_id: int, full_name: str, username: str = None) -> User:
    """Создание нового пользователя"""
    db = SessionLocal()
    try:
        user = User(
            user_id=user_id,
            full_name=full_name,
            username=username
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        return user
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка при создании пользователя: {e}")
        raise
    finally:
        db.close()


async def update_user_activity(user_id: int):
    """Обновление времени последней активности пользователя"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            user.last_activity = datetime.now()
            db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка при обновлении активности пользователя: {e}")
    finally:
        db.close()


async def increment_message_count(user_id: int):
    """Увеличение счетчика сообщений пользователя"""
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == user_id).first()
        if user:
            user.messages_count += 1
            db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка при увеличении счетчика сообщений: {e}")
    finally:
        db.close()


async def get_all_users() -> list[User]:
    """Получение всех пользователей"""
    db = SessionLocal()
    try:
        return db.query(User).all()
    finally:
        db.close()


async def get_active_users() -> list[User]:
    """Получение активных пользователей (активность за последние 24 часа)"""
    db = SessionLocal()
    try:
        from datetime import timedelta
        yesterday = datetime.now() - timedelta(days=1)
        return db.query(User).filter(User.last_activity >= yesterday).all()
    finally:
        db.close()


async def save_message(user_id: int, message_id: int, chat_id: int, message_type: str, content: str = None, file_id: str = None):
    """Сохранение сообщения в базу данных"""
    db = SessionLocal()
    try:
        message = Message(
            user_id=user_id,
            message_id=message_id,
            chat_id=chat_id,
            message_type=message_type,
            content=content,
            file_id=file_id
        )
        db.add(message)
        db.commit()
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка при сохранении сообщения: {e}")
    finally:
        db.close()
