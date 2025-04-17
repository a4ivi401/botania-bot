import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()

@dataclass
class Config:
    """Класс для хранения конфигурации бота."""
    TELEGRAM_TOKEN: str
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: str
    GOOGLE_API_KEY: str
    DEEPSEEK_API_KEY: str
    
    def __init__(self):
        """Инициализирует конфигурацию из переменных окружения."""
        self.TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN", "")
        self.OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
        self.ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
        self.GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
        self.DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "")
        
        # Проверка наличия обязательного токена Telegram
        if not self.TELEGRAM_TOKEN:
            raise ValueError("TELEGRAM_TOKEN не указан в переменных окружения")