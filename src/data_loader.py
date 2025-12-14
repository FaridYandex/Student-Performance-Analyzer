import pandas as pd
import os

def load_data(file_path: str) -> pd.DataFrame:
    """Загружает данные об успеваемости из CSV файла"""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Файл не найден: {file_path}")
    
    try:
        df = pd.read_csv(file_path)
        validate_data(df)
        return df
    except Exception as e:
        raise ValueError(f"Ошибка при загрузке данных: {str(e)}")

def validate_data(df: pd.DataFrame):
    """Проверяет корректность данных"""
    required_columns = ['student_id', 'subject', 'grade', 'attendance']
    if not all(col in df.columns for col in required_columns):
        raise ValueError(f"Отсутствуют обязательные столбцы: {required_columns}")
    
    if df['grade'].min() < 0 or df['grade'].max() > 100:
        raise ValueError("Оценки должны быть в диапазоне 0-100")
    
    if df['attendance'].min() < 0 or df['attendance'].max() > 100:
        raise ValueError("Посещаемость должна быть в диапазоне 0-100%")