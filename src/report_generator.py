import matplotlib.pyplot as plt
import pandas as pd
from jinja2 import Template
import os
from .analyzer import analyze_student_performance, get_class_statistics
from .recommender import generate_recommendations
from .utils.i18n import get_text


def generate_student_report(
    df: pd.DataFrame, student_id: int, output_path: str = "docs/report.html"
):
    """Генерирует HTML-отчет для студента"""
    performance = analyze_student_performance(df, student_id)
    recommendations = generate_recommendations(
        performance["weak_subjects"], performance["average_grade"]
    )
    class_stats = get_class_statistics(df)

    _generate_grade_chart(df, student_id, performance["average_grade"])

    template = Template(
        "<!DOCTYPE html>\n"
        "<html lang=\"ru\">\n"
        "<head>\n"
        "    <meta charset=\"UTF-8\">\n"
        "    <title>Отчет по успеваемости</title>\n"
        "    <style>\n"
        "        body { font-family: Arial, sans-serif; margin: 40px; }\n"
        "        .chart { text-align: center; margin: 30px 0; }\n"
        "        .recommendations { background-color: #f0f8ff; padding: 20px; "
        "border-radius: 8px; }\n"
        "        .risk-high { color: #dc3545; font-weight: bold; }\n"
        "        .risk-medium { color: #ffc107; font-weight: bold; }\n"
        "        .risk-low { color: #28a745; font-weight: bold; }\n"
        "    </style>\n"
        "</head>\n"
        "<body>\n"
        "    <h1>{{ title }}</h1>\n"
        "    <p><strong>Студент ID:</strong> {{ student_id }}</p>\n"
        "    <p><strong>Средний балл:</strong> {{ average_grade }} / 100</p>\n"
        "    <p><strong>Посещаемость:</strong> {{ attendance }}%</p>\n"
        "    <div class=\"chart\">\n"
        "        <img src=\"grade_chart.png\" alt=\"График успеваемости\" "
        "width=\"600\">\n"
        "    </div>\n"
        "    <h2>Слабые предметы:</h2>\n"
        "    <ul>\n"
        "        {% for subject in weak_subjects %}\n"
        "            <li>{{ subject }}</li>\n"
        "        {% endfor %}\n"
        "    </ul>\n"
        "    <h2>Уровень риска отчисления:</h2>\n"
        "    <p class=\"risk-{{ risk_level }}\">{{ risk_text }}</p>\n"
        "    <div class=\"recommendations\">\n"
        "        <h2>Рекомендуемые материалы:</h2>\n"
        "        <ul>\n"
        "            {% for rec in recommendations %}\n"
        "                <li><a href=\"{{ rec.url }}\" target=\"_blank\">"
        "{{ rec.title }}</a> (Сложность: {{ rec.difficulty }})</li>\n"
        "            {% endfor %}\n"
        "        </ul>\n"
        "    </div>\n"
        "    <h2>Статистика по классу:</h2>\n"
        "    <p>Всего студентов: {{ class_stats.total_students }}</p>\n"
        "    <p>Средний балл по классу: {{ class_stats.average_class_grade }}"
        "</p>\n"
        "    <p>Распределение рисков: Высокий - "
        "{{ class_stats.risk_distribution.high }}, Средний - "
        "{{ class_stats.risk_distribution.medium }}, Низкий - "
        "{{ class_stats.risk_distribution.low }}</p>\n"
        "</body>\n"
        "</html>"
    )

    risk_texts = {
        "high": get_text("risk_high"),
        "medium": get_text("risk_medium"),
        "low": get_text("risk_low"),
    }

    html_content = template.render(
        title=get_text("report_title"),
        student_id=student_id,
        average_grade=performance["average_grade"],
        attendance=performance["average_attendance"],
        weak_subjects=performance["weak_subjects"],
        risk_level=performance["risk_level"],
        risk_text=risk_texts[performance["risk_level"]],
        recommendations=recommendations,
        class_stats=class_stats,
    )

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html_content)


def _generate_grade_chart(df: pd.DataFrame, student_id: int, avg_grade: float):
    """Генерирует график успеваемости для отчета"""
    student_data = df[df["student_id"] == student_id]
    plt.figure(figsize=(10, 6))
    plt.bar(student_data["subject"], student_data["grade"], color="skyblue")
    plt.axhline(y=avg_grade, color="r", linestyle="--", label=f"Среднее: {avg_grade}")
    plt.title("Успеваемость по предметам")
    plt.xlabel("Предметы")
    plt.ylabel("Оценки")
    plt.ylim(0, 100)
    plt.legend()
    plt.tight_layout()
    plt.savefig("docs/grade_chart.png")
    plt.close()
