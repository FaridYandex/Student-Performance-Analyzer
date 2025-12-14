import pandas as pd
import os
from src.data_loader import load_data
from src.report_generator import generate_student_report
from src.utils.i18n import set_language

def main():
    print("Запуск генерации ежедневного отчета...")
    
    # Устанавливаем язык из переменной окружения
    lang = os.getenv("APP_LANGUAGE", "ru")
    set_language(lang)
    
    try:
        # Загружаем данные
        df = load_data("data/sample_grades.csv")
        
        # Генерируем отчеты для всех студентов
        for student_id in df['student_id'].unique():
            print(f"Генерация отчета для студента {student_id}...")
            generate_student_report(df, int(student_id), f"docs/report_student_{student_id}.html")
        
        print("✅ Все отчеты успешно сгенерированы!")
    except Exception as e:
        print(f"❌ Ошибка при генерации отчета: {str(e)}")
        exit(1)

if __name__ == "__main__":
    main()
    