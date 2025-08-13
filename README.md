# ChatBot Becks

Современный чат-бот для Telegram с расширенными возможностями.

## 🚀 Возможности

- 🤖 **AI-обработка текстовых сообщений** (OpenRouter API)
- 📸 **Анализ изображений** (Google Gemini 2.0 Flash)
- 📹 Поддержка медиа-файлов (фото, видео, документы)
- ⌨️ Инлайн-кнопки и клавиатуры
- 👨‍💼 Система команд администратора
- 📊 Логирование действий и статистика
- 🗄️ База данных для хранения информации
- 🎤 Обработка голосовых сообщений (планируется)

## 📋 Требования

- Python 3.8+
- Telegram Bot Token
- База данных (SQLite/PostgreSQL)

## 🛠 Установка

1. Клонируйте репозиторий:
```bash
git clone https://github.com/siberianesports-creator/chatbotbecks.git
cd chatbotbecks
```

2. Установите зависимости:
```bash
pip install -r requirements.txt
```

3. Создайте файл конфигурации:
```bash
cp config.example.py config.py
```

4. Настройте токен бота в `config.py`

5. Запустите бота:
```bash
python main.py
```

## 📁 Структура проекта

```
chatbotbecks/
├── main.py              # Главный файл запуска
├── bot.py               # Основная логика бота
├── config.py            # Конфигурация
├── handlers/            # Обработчики сообщений
│   ├── __init__.py
│   ├── text.py
│   ├── media.py
│   └── commands.py
├── keyboards/           # Клавиатуры
│   ├── __init__.py
│   └── reply.py
├── database/            # Работа с базой данных
│   ├── __init__.py
│   └── models.py
├── utils/               # Утилиты
│   ├── __init__.py
│   └── helpers.py
├── requirements.txt     # Зависимости
└── README.md           # Документация
```

## 🔧 Конфигурация

Создайте файл `config.py` со следующими параметрами:

```python
BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
ADMIN_IDS = [123456789]  # ID администраторов
DATABASE_URL = "sqlite:///bot.db"
```

## 📝 Использование

После запуска бот будет отвечать на сообщения и выполнять команды:

- `/start` - Начать работу с ботом
- `/help` - Показать справку
- `/admin` - Панель администратора (только для админов)

## 🤝 Вклад в проект

1. Форкните репозиторий
2. Создайте ветку для новой функции
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

MIT License

## 👨‍💻 Автор

Siberian Esports Creator
