FROM python:3.12-slim

# Установка системных зависимостей
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        postgresql-client \
        build-essential \
        libpq-dev \
        gettext \
    && rm -rf /var/lib/apt/lists/*

# Создание рабочей директории
WORKDIR /app

# Копирование файлов зависимостей
COPY requirements.txt .

# Установка Python зависимостей
RUN pip install --no-cache-dir -r requirements.txt

# Копирование проекта
COPY . .

# Создание директории для статических файлов
RUN mkdir -p /app/static /app/media

# Создание пользователя для безопасности
RUN adduser --disabled-password --gecos '' appuser \
    && chown -R appuser:appuser /app
USER appuser

# Открытие порта
EXPOSE 8000

# Команда запуска
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
