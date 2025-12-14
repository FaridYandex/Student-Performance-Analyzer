import json
import os
from typing import List, Dict

def load_curriculum() -> Dict[str, List[Dict]]:
    """Загружает учебные материалы из JSON"""
    with open('data/curriculum.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def generate_recommendations(weak_subjects: List[str], avg_grade: float) -> List[Dict]:
    """Генерирует персонализированные рекомендации"""
    curriculum = load_curriculum()
    recommendations = []
    
    for subject in weak_subjects:
        if subject in curriculum:
            # Выбираем материалы в зависимости от общего уровня успеваемости
            if avg_grade < 60:
                # Для низких оценок - базовые материалы
                recs = [m for m in curriculum[subject] if m['difficulty'] == 'beginner']
            elif avg_grade < 80:
                # Для средних оценок - смешанные материалы
                recs = [m for m in curriculum[subject] if m['difficulty'] in ['beginner', 'intermediate']]
            else:
                # Для высоких оценок - продвинутые материалы
                recs = curriculum[subject]
            
            recommendations.extend(recs[:2])  # Берем максимум 2 рекомендации на предмет
    
    return recommendations