from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def create_models_keyboard(models: dict) -> InlineKeyboardMarkup:
    """Создает клавиатуру с кнопками для выбора модели ИИ.
    
    Args:
        models: Словарь доступных моделей (ключ: название)
        
    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопками моделей
    """
    kb = InlineKeyboardBuilder()
    
    for model_id, name in models.items():
        kb.button(text=name, callback_data=model_id)
    
    # Располагаем кнопки в один столбец
    kb.adjust(1)
    
    return kb.as_markup()

def create_change_model_keyboard() -> InlineKeyboardMarkup:
    """Создает клавиатуру с кнопкой для смены модели.
    
    Returns:
        InlineKeyboardMarkup: Клавиатура с кнопкой смены модели
    """
    kb = InlineKeyboardBuilder()
    kb.button(text="🔄 Выбрать другую модель", callback_data="change_model")
    
    return kb.as_markup()