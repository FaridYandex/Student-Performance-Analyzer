import matplotlib.pyplot as plt
import pandas as pd
from jinja2 import Template
import os
from .analyzer import analyze_student_performance, get_class_statistics
from .recommender import generate_recommendations
from .utils.i18n import get_text

def generate_student_report(df: pd.DataFrame, student_id: int, output_path: str = "docs/report.html"):
    """Генерирует HTML-отчет для студента"""
    # Анализ данных
    performance = analyze_student_performance(df, student_id)
    recommendations = generate_recommendations(performance['weak_subjects'], performance['average_grade'])
    class_stats = get_class_statistics(df)
    
    # Генерация графиков
    _generate_grade_chart(df, student_id, performance['average_grade'])
    
    # HTML-шаблон
    template = Template("""
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <title>Отчет по успеваемости</title>
        <style>
            body { font-family: Arial, sans-serif; margin: 40px; }
            .chart { text-align: center; margin: 30px 0; }
            .recommendations { background-color: #f0f8ff; padding: 20px; border-radius: 8px; }
            .risk-high { color: #dc3545; font-weight: bold; }
            .risk-medium { color: #ffc107; font-weight: bold; }
            .risk-low { color: #28a745; font-weight: bold; }
        </style>
    </head>
    <body>
        <h1>{{ title }}</h1>
        <p><strong>Студент ID:</strong> {{ student_id }}</p>
        <p><strong>Средний балл:</strong> {{ average_grade }} / 100</p>
        <p><strong>Посещаемость:</strong> {{ attendance }}%</p>
        
        <div class="chart">
            <img src="grade_chart.png" alt="График успеваемости" width="600">
        </div>
        
        <h2>Слабые предметы:</h2>
        <ul>
            {% for subject in weak_subjects %}
                <li>{{ subject }}</li>
            {% endfor %}
        </ul>
        
        <h2>Уровень риска отчисления:</h2>
        <p class="risk-{{ risk_level }}">{{ risk_text }}</p>
        
        <div class="recommendations">
            <h2>Рекомендуемые материалы:</h2>
            <ul>
                {% for rec in recommendations %}
                    <li><a href="{{ rec.url }}" target="_blank">{{ rec.title }}</a> (Сложность: {{ rec.difficulty }})</li>
                {% endfor %}
            </ul>
        </div>
        
        <h2>Статистика по классу:</h2>
        <p>Всего студентов: {{ class_stats.total_students }}</p>
        <p>Средний балл по классу: {{ class_stats.average_class_grade }}</p>
        <p>Распределение рисков: Высокий - {{ class_stats.risk_distribution.high }}, 
           Средний - {{ class_stats.risk_distribution.medium }}, 
           Низкий - {{ class_stats.risk_distribution.low }}</p>
    </body>
    </html>
    """)
    
    # Определение текста риска с локализацией
    risk_texts = {
        "high": get_text("risk_high"),
        "medium": get_text("risk_medium"),
        "low": get_text("risk_low")
    }
    
    # Генерация HTML
    html_content = template.render(
        title=get_text("report_title"),
        student_id=student_id,
        average_grade=performance['average_grade'],
        attendance=performance['average_attendance'],
        weak_subjects=performance['weak_subjects'],
        risk_level=performance['risk_level'],
        risk_text=risk_texts[performance['risk_level']],
        recommendations=recommendations,
        class_stats=class_stats
    )
    
    # Сохранение отчета
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

def _generate_grade_chart(df: pd.DataFrame, student_id: int, avg_grade: float):
    """Генерирует график успеваемости для отчета"""
    student_data = df[df['student_id'] == student_id]
    
    plt.figure(figsize=(10, 6))
    plt.bar(student_data['subject'], student_data['grade'], color='skyblue')
    plt.axhline(y=avg_grade, color='r', linestyle='--', label=f'Среднее: {avg_grade}')
    plt.title('Успеваемость по предметам')
    plt.xlabel('Предметы')
    plt.ylabel('Оценки')
    plt.ylim(0, 100)
    plt.legend()
    plt.tight_layout()
    plt.savefig('docs/grade_chart.png')
    plt.close()