"""
Клавиатуры для бота
"""

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """Основная клавиатура"""
    keyboard = [
        [
            KeyboardButton(text="📚 Помощь"),
            KeyboardButton(text="👤 Профиль")
        ],
        [
            KeyboardButton(text="⚙️ Настройки"),
            KeyboardButton(text="📞 Контакты")
        ],
        [
            KeyboardButton(text="💬 Обратная связь"),
            KeyboardButton(text="ℹ️ О боте")
        ]
    ]
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Выберите действие или напишите сообщение"
    )


def get_admin_keyboard() -> ReplyKeyboardMarkup:
    """Клавиатура администратора"""
    keyboard = [
        [
            KeyboardButton(text="📊 Статистика"),
            KeyboardButton(text="👥 Пользователи")
        ],
        [
            KeyboardButton(text="📢 Рассылка"),
            KeyboardButton(text="🔧 Управление")
        ],
        [
            KeyboardButton(text="⬅️ Назад"),
            KeyboardButton(text="🔄 Перезапуск")
        ]
    ]
    
    return ReplyKeyboardMarkup(
        keyboard=keyboard,
        resize_keyboard=True,
        input_field_placeholder="Панель администратора"
    )


def get_settings_keyboard() -> InlineKeyboardMarkup:
    """Инлайн клавиатура настроек"""
    keyboard = [
        [
            InlineKeyboardButton(text="🔔 Уведомления", callback_data="settings_notifications"),
            InlineKeyboardButton(text="🌍 Язык", callback_data="settings_language")
        ],
        [
            InlineKeyboardButton(text="🔒 Приватность", callback_data="settings_privacy"),
            InlineKeyboardButton(text="📱 Интерфейс", callback_data="settings_interface")
        ],
        [
            InlineKeyboardButton(text="❌ Закрыть", callback_data="settings_close")
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_help_keyboard() -> InlineKeyboardMarkup:
    """Инлайн клавиатура помощи"""
    keyboard = [
        [
            InlineKeyboardButton(text="📖 Команды", callback_data="help_commands"),
            InlineKeyboardButton(text="❓ FAQ", callback_data="help_faq")
        ],
        [
            InlineKeyboardButton(text="📞 Поддержка", callback_data="help_support"),
            InlineKeyboardButton(text="🌐 Сайт", url="https://github.com/siberianesports-creator/chatbotbecks")
        ],
        [
            InlineKeyboardButton(text="❌ Закрыть", callback_data="help_close")
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_broadcast_keyboard() -> InlineKeyboardMarkup:
    """Инлайн клавиатура для рассылки"""
    keyboard = [
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data="broadcast_confirm"),
            InlineKeyboardButton(text="❌ Отменить", callback_data="broadcast_cancel")
        ]
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)
