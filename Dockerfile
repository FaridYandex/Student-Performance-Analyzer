FROM python:3.10

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Установка системных зависимостей (если используете matplotlib)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libgl1 libglib2.0-0 libsm6 libxext6 libxrender-dev libgomp1 && \
    rm -rf /var/lib/apt/lists/*

COPY . .

# 🔥 КЛЮЧЕВАЯ СТРОКА: говорим Python, где искать модули
ENV PYTHONPATH=/app

ENV MPLBACKEND=Agg

CMD ["python", "scripts/generate_daily_report.py"]docker build -t student-analyzer .