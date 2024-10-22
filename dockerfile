# Используем официальный образ Python в качестве базового
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY . /app

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Копируем файл .env в контейнер
COPY .env /app/.env

# Устанавливаем переменные окружения
ENV BOT_TOKEN='7806759833:AAHPW0S0H467QwjZsiFfgU-1p3-7ILoluFQ'
ENV GPT_TOKEN='sk-proj-pbjwFBphIcsYWH0B6wtWT3BlbkFJoi4bqWhzw6lYyAXWk5r5'
ENV ASSISTANT_ID='asst_sCYeiJcWHkrMsm0I5bv8qauM'
ENV WEBHOOK_URL='https://f4c5-212-58-102-223.ngrok-free.app/webhook'

# Запускаем приложение
CMD ["python", "webhook.py"]