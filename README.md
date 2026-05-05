# 🚀 FastAPI User Management API

Простой и эффективный пет-проект на **FastAPI** для управления списком пользователей. Реализовано взаимодействие с **PostgreSQL** через асинхронный драйвер `asyncpg`, контейнеризация через **Docker** и валидация данных с помощью **Pydantic**.

## ✨ Особенности
- **Асинхронность**: Полностью неблокирующий код с использованием `asyncpg`.
- **🚀 Производительность**: Middleware для отслеживания медленных запросов (> 100мс).
- **🛡 Валидация**: Строгая проверка email, возраста и имен через Pydantic-схемы.
- **🐳 Docker Ready**: Готовый `docker-compose` для быстрого развертывания базы и приложения.
- **📊 Database**: Автоматическое создание таблиц и индексов при старте (Lifespan события).

## 🛠 Технологический стек
- **Backend**: FastAPI, Uvicorn.
- **Database**: PostgreSQL 15.
- **Environment**: Python-dotenv (управление секретами).
- **Deployment**: Docker, Docker Compose.

## 📋 Эндпоинты (API)
- `GET /` — Проверка состояния сервера (Healthcheck).
- `GET /users` — Получение списка всех пользователей (сортировка по времени регистрации).
- `POST /add_user` — Регистрация нового пользователя.
- `DELETE /delete_user` — Удаление конкретного пользователя (требуется админ-пароль).
- `DELETE /clear` — Полная очистка базы данных (требуется админ-пароль).

## 🚀 Быстрый запуск

### 1. Подготовка окружения
Создайте файл `.env` в корневой папке проекта:
```env
DB_USER=postgres
DB_PASSWORD=mysecretpassword
DB_NAME=user_db
ADMIN_PASSWORD=superadmin
DATABASE_URL=postgresql://postgres:mysecretpassword@db:5432/user_db
```

### 2. Запуск через Docker
Убедитесь, что у вас установлен Docker, и выполните команду:
```bash
docker-compose up --build
```
После запуска API будет доступна по адресу: [http://localhost:8000](http://localhost:8000)

### 3. Документация
FastAPI автоматически генерирует интерактивную документацию:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## 📁 Структура проекта
- `main.py` — Инициализация FastAPI, маршруты и Middleware.
- `db.py` — Логика работы с базой данных, управление пулом соединений.
- `schemas.py` — Pydantic модели для валидации входящих и исходящих данных.
- `docker-compose.yml` & `Dockerfile` — Конфигурация контейнеризации.

---
*Разработано в качестве пет-проекта для изучения современных подходов в разработке API.*