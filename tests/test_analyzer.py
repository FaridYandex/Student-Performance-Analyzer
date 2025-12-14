import pandas as pd
from src.analyzer import analyze_student_performance, get_class_statistics


def test_analyze_student_performance():
    """Тест анализа успеваемости для студента"""
    data = {
        "student_id": [1, 1, 2, 2],
        "subject": ["Math", "Physics", "Math", "Physics"],
        "grade": [85, 70, 90, 60],
        "attendance": [95, 85, 90, 75],
    }
    df = pd.DataFrame(data)

    result = analyze_student_performance(df, 1)
    assert result["student_id"] == 1
    assert result["average_grade"] == 77.5
    assert result["average_attendance"] == 90.0
    assert result["weak_subjects"] == ["Physics"]  # Physics имеет оценку 70 < 75
    assert result["risk_level"] in ["high", "medium", "low"]


def test_get_class_statistics():
    """Тест статистики по классу"""
    data = {
        "student_id": [1, 1, 2, 2, 3, 3],
        "subject": ["Math", "Physics", "Math", "Physics", "Math", "Physics"],
        "grade": [85, 70, 90, 60, 50, 55],
        "attendance": [95, 85, 90, 75, 60, 65],
    }
    df = pd.DataFrame(data)

    stats = get_class_statistics(df)
    assert stats["total_students"] == 3
    assert 50 < stats["average_class_grade"] < 70
    assert len(stats["subjects"]) == 2
    assert stats["risk_distribution"]["high"] >= 1  # Студент 3 имеет низкие оценки
