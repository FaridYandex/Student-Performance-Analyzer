import json
import os
from typing import Dict

# Глобальная переменная для языка
_current_language = os.getenv("APP_LANGUAGE", "en")


def set_language(lang: str):
    """Устанавливает текущий язык"""
    global _current_language
    if lang not in ["en", "ru"]:
        raise ValueError("Поддерживаемые языки: en, ru")
    _current_language = lang


def _load_translations() -> Dict[str, Dict]:
    """Загружает все переводы"""
    translations = {}
    for lang in ["en", "ru"]:
        file_path = f"locales/{lang}.json"
        if os.path.exists(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                translations[lang] = json.load(f)
    return translations


_translations = _load_translations()


def get_text(key: str) -> str:
    """Получает текст на текущем языке"""
    if _current_language not in _translations:
        return f"[{_current_language}]{key}"

    return _translations[_current_language].get(key, f"[MISSING:{key}]")
