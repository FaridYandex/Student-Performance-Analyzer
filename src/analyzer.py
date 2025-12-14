import pandas as pd
from typing import Dict, Any


def analyze_student_performance(df: pd.DataFrame, student_id: int) -> Dict[str, Any]:
    """Анализирует успеваемость студента"""
    student_data = df[df["student_id"] == student_id]

    if student_data.empty:
        raise ValueError(f"Студент с ID {student_id} не найден")

    avg_grade = student_data["grade"].mean()
    avg_attendance = student_data["attendance"].mean()

    # Определяем слабые предметы (оценка < 70)
    weak_subjects = student_data[student_data["grade"] < 70]["subject"].tolist()

    # Прогноз риска отчисления (простая эвристика)
    risk_score = (100 - avg_grade) * 0.6 + (100 - avg_attendance) * 0.4
    risk_level = "high" if risk_score > 60 else "medium" if risk_score > 30 else "low"

    return {
        "student_id": student_id,
        "average_grade": round(avg_grade, 2),
        "average_attendance": round(avg_attendance, 2),
        "weak_subjects": weak_subjects,
        "risk_level": risk_level,
        "risk_score": round(risk_score, 2),
    }


def get_class_statistics(df: pd.DataFrame) -> Dict[str, Any]:
    """Статистика по всему классу"""
    return {
        "total_students": df["student_id"].nunique(),
        "average_class_grade": round(df["grade"].mean(), 2),
        "subjects": df["subject"].unique().tolist(),
        "risk_distribution": {
            "high": len(
                df.groupby("student_id")
                .filter(
                    lambda x: (100 - x["grade"].mean()) * 0.6
                    + (100 - x["attendance"].mean()) * 0.4
                    > 60
                )["student_id"]
                .unique()
            ),
            "medium": len(
                df.groupby("student_id")
                .filter(
                    lambda x: 30
                    < (100 - x["grade"].mean()) * 0.6
                    + (100 - x["attendance"].mean()) * 0.4
                    <= 60
                )["student_id"]
                .unique()
            ),
            "low": len(
                df.groupby("student_id")
                .filter(
                    lambda x: (100 - x["grade"].mean()) * 0.6
                    + (100 - x["attendance"].mean()) * 0.4
                    <= 30
                )["student_id"]
                .unique()
            ),
        },
    }
