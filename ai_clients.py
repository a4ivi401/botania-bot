import logging
import openai
import anthropic
import google.generativeai as genai
from typing import Dict, Any, Optional

from config import Config

# Настройка логирования
logger = logging.getLogger(__name__)

# Загрузка конфигурации
config = Config()

# Инициализация клиентов API
openai.api_key = config.OPENAI_API_KEY
anthropic_client = anthropic.Anthropic(api_key=config.ANTHROPIC_API_KEY)
genai.configure(api_key=config.GOOGLE_API_KEY)

# Заглушка для DeepSeek (замените на реальный клиент)
class DeepSeekClient:
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    async def generate(self, prompt: str) -> str:
        """Заглушка для DeepSeek API."""
        # В реальном коде здесь должен быть запрос к DeepSeek API
        return f"Ответ от DeepSeek на запрос: {prompt[:50]}..."

deepseek_client = DeepSeekClient(api_key=config.DEEPSEEK_API_KEY)

async def ask_chatgpt(query: str) -> str:
    """Отправляет запрос к ChatGPT и возвращает ответ.
    
    Args:
        query: Текст запроса
        
    Returns:
        str: Ответ от модели
    """
    try:
        response = await openai.ChatCompletion.acreate(
            model="gpt-4",
            messages=[{"role": "user", "content": query}],
            max_tokens=1000
        )
        return response.choices[0].message.content
    except Exception as e:
        logger.error(f"Ошибка при запросе к ChatGPT: {e}")
        return f"❌ Произошла ошибка при обращении к ChatGPT: {str(e)}"

async def ask_claude(query: str) -> str:
    """Отправляет запрос к Claude AI и возвращает ответ.
    
    Args:
        query: Текст запроса
        
    Returns:
        str: Ответ от модели
    """
    try:
        response = anthropic_client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=1000,
            messages=[{"role": "user", "content": query}]
        )
        return response.content[0].text
    except Exception as e:
        logger.error(f"Ошибка при запросе к Claude: {e}")
        return f"❌ Произошла ошибка при обращении к Claude AI: {str(e)}"

async def ask_gemini(query: str) -> str:
    """Отправляет запрос к Gemini и возвращает ответ.
    
    Args:
        query: Текст запроса
        
    Returns:
        str: Ответ от модели
    """
    try:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(query)
        return response.text
    except Exception as e:
        logger.error(f"Ошибка при запросе к Gemini: {e}")
        return f"❌ Произошла ошибка при обращении к Gemini: {str(e)}"

async def ask_deepseek(query: str) -> str:
    """Отправляет запрос к DeepSeek и возвращает ответ.
    
    Args:
        query: Текст запроса
        
    Returns:
        str: Ответ от модели
    """
    try:
        response = await deepseek_client.generate(query)
        return response
    except Exception as e:
        logger.error(f"Ошибка при запросе к DeepSeek: {e}")
        return f"❌ Произошла ошибка при обращении к DeepSeek: {str(e)}"