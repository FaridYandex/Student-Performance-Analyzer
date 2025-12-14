from src.utils.i18n import set_language, get_text, _load_translations


def test_language_switching():
    """Тест переключения языков"""
    # Проверяем английский
    set_language("en")
    assert get_text("welcome_message") == "Welcome to the Student Performance Analyzer!"
    
    # Проверяем русский
    set_language("ru")
    assert get_text("welcome_message") == "Добро пожаловать в систему анализа успеваемости!"
    
    # Проверяем обработку отсутствующего ключа
    assert "MISSING" in get_text("non_existent_key")


def test_load_translations():
    """Тест загрузки переводов"""
    translations = _load_translations()
    assert "en" in translations
    assert "ru" in translations
    assert "welcome_message" in translations["en"]