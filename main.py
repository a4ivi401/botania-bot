import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import Config
from keyboards import create_models_keyboard, create_change_model_keyboard
from ai_clients import ask_chatgpt, ask_claude, ask_gemini, ask_deepseek

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация роутера
router = Router()

# Определение состояний
class BotaniaStates(StatesGroup):
    choosing_model = State()
    awaiting_query = State()

# Доступные модели
MODELS = {
    "chatgpt": "🤖 ChatGPT (OpenAI)",
    "claude": "🧠 Claude AI (Anthropic)",
    "gemini": "✨ Gemini (Google)",
    "deepseek": "🔍 DeepSeek AI"
}

# Обработчик команды /start
@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Приветственное сообщение и выбор модели."""
    user = message.from_user
    welcome_message = (
        f"🌟 Привет, {user.first_name}! 🌟\n\n"
        f"🌱 Добро пожаловать в Botania - твой проводник в мир искусственного интеллекта. 🌱\n\n"
        f"🤔 Я помогу тебе общаться с различными моделями ИИ. Выбери модель из списка ниже:"
    )
    
    # Создаем клавиатуру с моделями
    keyboard = create_models_keyboard(MODELS)
    
    await message.answer(welcome_message, reply_markup=keyboard)
    await state.set_state(BotaniaStates.choosing_model)

# Обработчик выбора модели
@router.callback_query(BotaniaStates.choosing_model)
async def process_model_choice(callback: CallbackQuery, state: FSMContext):
    """Обрабатывает выбор модели и переходит к ожиданию запроса."""
    model_id = callback.data
    
    # Проверяем, что модель существует
    if model_id not in MODELS:
        await callback.answer("❌ Неверный выбор модели", show_alert=True)
        return
    
    # Сохраняем выбранную модель
    await state.update_data(model=model_id)
    
    model_name = MODELS[model_id]
    await callback.message.edit_text(
        f"✅ Вы выбрали модель: {model_name}\n\n"
        f"💬 Теперь введите ваш запрос, и я передам его выбранной модели."
    )
    await callback.answer()
    
    await state.set_state(BotaniaStates.awaiting_query)

# Обработчик текстовых сообщений
@router.message(BotaniaStates.awaiting_query, F.text)
async def process_query(message: Message, state: FSMContext):
    """Обрабатывает запрос пользователя и отправляет его выбранной модели."""
    user_data = await state.get_data()
    model = user_data.get("model")
    
    if not model:
        await message.answer("❌ Модель не выбрана. Используйте /start для выбора модели.")
        return
    
    # Отправляем сообщение "печатает..."
    await message.answer("🔄 Обрабатываю ваш запрос...")
    
    # Определяем, какую модель использовать для ответа
    if model == "chatgpt":
        response = await ask_chatgpt(message.text)
    elif model == "claude":
        response = await ask_claude(message.text)
    elif model == "gemini":
        response = await ask_gemini(message.text)
    elif model == "deepseek":
        response = await ask_deepseek(message.text)
    else:
        response = "❓ Неизвестная модель. Используйте /start для выбора модели."
    
    # Отправляем ответ пользователю
    await message.answer(f"🤖 Ответ от {MODELS[model]}:\n\n{response}")
    
    # Предлагаем пользователю выбрать другую модель
    keyboard = create_change_model_keyboard()
    await message.answer("🔄 Хотите выбрать другую модель?", reply_markup=keyboard)

# Обработчик для смены модели
@router.callback_query(BotaniaStates.awaiting_query, F.data == "change_model")
async def process_change_model(callback: CallbackQuery, state: FSMContext):
    """Позволяет пользователю выбрать другую модель."""
    keyboard = create_models_keyboard(MODELS)
    
    await callback.message.edit_text(
        "🔍 Выберите модель ИИ из списка ниже:", 
        reply_markup=keyboard
    )
    await callback.answer()
    
    await state.set_state(BotaniaStates.choosing_model)

# Обработчик команды /help
@router.message(Command("help"))
async def cmd_help(message: Message):
    """Отправляет сообщение с помощью при получении команды /help."""
    help_text = (
        "🤖 *Botania - Помощник* 🌱\n\n"
        "Доступные команды:\n"
        "🚀 /start - Начать диалог и выбрать модель ИИ\n"
        "❓ /help - Показать это сообщение помощи\n\n"
        "Как использовать бота:\n"
        "1️⃣ Выберите модель ИИ из предложенного списка\n"
        "2️⃣ Введите ваш запрос\n"
        "3️⃣ Получите ответ от выбранной модели\n\n"
        "🔄 В любой момент вы можете сменить модель, нажав на кнопку 'Выбрать другую модель'"
    )
    await message.answer(help_text, parse_mode="MarkdownV2")

async def main():
    """Точка входа в программу."""
    # Загрузка конфигурации
    config = Config()
    
    # Инициализация бота и диспетчера
    bot = Bot(token=config.TELEGRAM_TOKEN)
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(router)
    
    # Запуск бота
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())