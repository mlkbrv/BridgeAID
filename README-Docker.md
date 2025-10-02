# BridgeAID Docker Setup

Этот проект настроен для запуска в Docker контейнерах с использованием Docker Compose.

## Быстрый старт

### 1. Клонирование и настройка

```bash
git clone <your-repo>
cd BridgeAID
cp env.example .env
```

### 2. Редактирование переменных окружения

Отредактируйте файл `.env` и установите нужные значения:

```bash
# Основные настройки
DEBUG=1
SECRET_KEY=your-secret-key-here
POSTGRES_PASSWORD=your-secure-password

# Дополнительные настройки (опционально)
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password
```

### 3. Запуск в режиме разработки

```bash
# Запуск всех сервисов
docker-compose -f docker-compose.dev.yml up --build

# Или в фоновом режиме
docker-compose -f docker-compose.dev.yml up -d --build
```

### 4. Создание суперпользователя

```bash
# В отдельном терминале
docker-compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
```

### 5. Запуск команды популяции данных

```bash
docker-compose -f docker-compose.dev.yml exec web python manage.py populate_db
```

## Продакшн развертывание

### 1. Подготовка

```bash
# Создайте SSL сертификаты
mkdir ssl
# Поместите ваши SSL сертификаты в папку ssl/
# cert.pem - сертификат
# key.pem - приватный ключ
```

### 2. Настройка переменных окружения

```bash
# Для продакшна установите
DEBUG=0
SECRET_KEY=your-very-secure-secret-key
POSTGRES_PASSWORD=your-very-secure-password
```

### 3. Запуск

```bash
# Запуск продакшн версии
docker-compose -f docker-compose.prod.yml up -d --build
```

## Доступные сервисы

После запуска будут доступны:

- **Веб-приложение**: http://localhost:8000
- **API**: http://localhost:8000/api/
- **Админка**: http://localhost:8000/admin/
- **PostgreSQL**: localhost:5432
- **Redis**: localhost:6379

## Полезные команды

### Управление контейнерами

```bash
# Просмотр логов
docker-compose logs -f web

# Остановка всех сервисов
docker-compose down

# Остановка с удалением volumes
docker-compose down -v

# Перезапуск сервиса
docker-compose restart web

# Выполнение команд в контейнере
docker-compose exec web python manage.py shell
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py collectstatic
```

### Работа с базой данных

```bash
# Подключение к PostgreSQL
docker-compose exec db psql -U bridgeaid -d bridgeaid

# Создание резервной копии
docker-compose exec db pg_dump -U bridgeaid bridgeaid > backup.sql

# Восстановление из резервной копии
docker-compose exec -T db psql -U bridgeaid bridgeaid < backup.sql
```

### Отладка

```bash
# Просмотр всех контейнеров
docker-compose ps

# Просмотр логов конкретного сервиса
docker-compose logs web
docker-compose logs db
docker-compose logs nginx

# Вход в контейнер
docker-compose exec web bash
docker-compose exec db bash
```

## Структура файлов

```
BridgeAID/
├── Dockerfile                 # Основной Dockerfile
├── docker-compose.yml         # Продакшн конфигурация
├── docker-compose.dev.yml     # Разработка конфигурация
├── docker-compose.prod.yml    # Продакшн конфигурация
├── nginx.conf                 # Nginx для разработки
├── nginx.prod.conf            # Nginx для продакшна
├── requirements.txt           # Python зависимости
├── .dockerignore             # Исключения для Docker
├── env.example               # Пример переменных окружения
└── README-Docker.md          # Эта документация
```

## Безопасность

### Для продакшна обязательно:

1. Измените `SECRET_KEY` на случайную строку
2. Установите `DEBUG=0`
3. Используйте сильные пароли для базы данных
4. Настройте SSL сертификаты
5. Ограничьте доступ к портам базы данных
6. Регулярно обновляйте образы

### Переменные окружения

- `SECRET_KEY` - секретный ключ Django
- `DEBUG` - режим отладки (0/1)
- `POSTGRES_PASSWORD` - пароль для PostgreSQL
- `DATABASE_URL` - URL подключения к базе данных
- `REDIS_URL` - URL подключения к Redis

## Мониторинг

### Health checks

Все сервисы имеют health checks:

```bash
# Проверка состояния
docker-compose ps
```

### Логи

```bash
# Все логи
docker-compose logs

# Логи конкретного сервиса
docker-compose logs web
```

## Troubleshooting

### Проблемы с подключением к базе данных

```bash
# Проверка состояния базы данных
docker-compose exec db pg_isready -U bridgeaid

# Перезапуск базы данных
docker-compose restart db
```

### Проблемы с миграциями

```bash
# Применение миграций
docker-compose exec web python manage.py migrate

# Создание новых миграций
docker-compose exec web python manage.py makemigrations
```

### Проблемы с статическими файлами

```bash
# Сбор статических файлов
docker-compose exec web python manage.py collectstatic --noinput
```

### Очистка и пересборка

```bash
# Полная очистка и пересборка
docker-compose down -v
docker system prune -f
docker-compose up --build
```
