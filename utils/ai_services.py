"""
Модуль для работы с AI сервисами
"""

import aiohttp
import json
import base64
from typing import Optional, Dict, Any
from loguru import logger

from config import (
    OPENROUTER_API_KEY, 
    GEMINI_API_KEY, 
    OPENROUTER_BASE_URL, 
    GEMINI_BASE_URL
)


class AIServices:
    """Класс для работы с AI сервисами"""
    
    def __init__(self):
        self.openrouter_api_key = OPENROUTER_API_KEY
        self.gemini_api_key = GEMINI_API_KEY
        self.openrouter_url = OPENROUTER_BASE_URL
        self.gemini_url = GEMINI_BASE_URL
    
    async def get_openrouter_response(self, prompt: str, model: str = "anthropic/claude-3.5-sonnet") -> Optional[str]:
        """
        Получение ответа от OpenRouter API
        
        Args:
            prompt: Текст запроса
            model: Модель для использования
            
        Returns:
            Ответ от AI или None при ошибке
        """
        try:
            headers = {
                "Authorization": f"Bearer {self.openrouter_api_key}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://github.com/siberianesports-creator/chatbotbecks",
                "X-Title": "ChatBot Becks"
            }
            
            data = {
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 1000,
                "temperature": 0.7
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    f"{self.openrouter_url}/chat/completions",
                    headers=headers,
                    json=data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result["choices"][0]["message"]["content"]
                    else:
                        logger.error(f"OpenRouter API error: {response.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error calling OpenRouter API: {e}")
            return None
    
    async def analyze_image_with_gemini(self, image_data: bytes, prompt: str = "Опиши это изображение") -> Optional[str]:
        """
        Анализ изображения с помощью Google Gemini
        
        Args:
            image_data: Байты изображения
            prompt: Запрос для анализа
            
        Returns:
            Описание изображения или None при ошибке
        """
        try:
            # Кодируем изображение в base64
            image_base64 = base64.b64encode(image_data).decode('utf-8')
            
            headers = {
                "Content-Type": "application/json"
            }
            
            data = {
                "contents": [
                    {
                        "parts": [
                            {
                                "text": prompt
                            },
                            {
                                "inline_data": {
                                    "mime_type": "image/jpeg",
                                    "data": image_base64
                                }
                            }
                        ]
                    }
                ],
                "generationConfig": {
                    "temperature": 0.4,
                    "topK": 32,
                    "topP": 1,
                    "maxOutputTokens": 2048,
                }
            }
            
            url = f"{self.gemini_url}/gemini-2.0-flash-exp:generateContent?key={self.gemini_api_key}"
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, headers=headers, json=data) as response:
                    if response.status == 200:
                        result = await response.json()
                        if "candidates" in result and result["candidates"]:
                            return result["candidates"][0]["content"]["parts"][0]["text"]
                        else:
                            logger.error("No response from Gemini API")
                            return None
                    else:
                        logger.error(f"Gemini API error: {response.status}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error calling Gemini API: {e}")
            return None
    
    async def get_smart_response(self, user_message: str, context: str = "") -> str:
        """
        Получение умного ответа на сообщение пользователя
        
        Args:
            user_message: Сообщение пользователя
            context: Контекст разговора
            
        Returns:
            Умный ответ от AI
        """
        prompt = f"""
Ты - дружелюбный и полезный Telegram бот ChatBot Becks. 
Отвечай кратко, дружелюбно и с эмодзи.

Контекст: {context}
Сообщение пользователя: {user_message}

Ответь как умный помощник, который может:
- Поддерживать разговор
- Давать полезные советы
- Отвечать на вопросы
- Быть вежливым и дружелюбным

Ответ должен быть на русском языке и не длиннее 200 символов.
"""
        
        response = await self.get_openrouter_response(prompt)
        if response:
            return response.strip()
        else:
            # Fallback ответ
            return "Извините, у меня временные проблемы с AI. Попробуйте позже! 🤖"
    
    async def analyze_product_from_image(self, image_data: bytes) -> Dict[str, Any]:
        """
        Анализ продукта на изображении
        
        Args:
            image_data: Байты изображения
            
        Returns:
            Словарь с информацией о продукте
        """
        prompt = """
Проанализируй это изображение и определи:
1. Что это за продукт/объект
2. Основные характеристики
3. Возможное использование

Ответь в формате JSON:
{
    "product_name": "название продукта",
    "description": "краткое описание",
    "characteristics": ["характеристика1", "характеристика2"],
    "usage": "как используется"
}
"""
        
        response = await self.analyze_image_with_gemini(image_data, prompt)
        if response:
            try:
                # Пытаемся извлечь JSON из ответа
                if "{" in response and "}" in response:
                    start = response.find("{")
                    end = response.rfind("}") + 1
                    json_str = response[start:end]
                    return json.loads(json_str)
                else:
                    return {
                        "product_name": "Неизвестный продукт",
                        "description": response,
                        "characteristics": [],
                        "usage": "Не определено"
                    }
            except json.JSONDecodeError:
                return {
                    "product_name": "Неизвестный продукт",
                    "description": response,
                    "characteristics": [],
                    "usage": "Не определено"
                }
        else:
            return {
                "product_name": "Не удалось распознать",
                "description": "Ошибка анализа изображения",
                "characteristics": [],
                "usage": "Не определено"
            }


# Создаем глобальный экземпляр
ai_services = AIServices()
