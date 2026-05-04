# ⚡️ FastAPI User Management API ⚡️

![FastAPI](https://shields.io)
![PostgreSQL](https://shields.io)
![Pydantic](https://shields.io)

Асинхронный сервис для управления данными пользователей с автоматическим созданием таблиц и мониторингом производительности.

---

## 💎 Основные возможности

🔹 **Database Pooling** — эффективное управление соединениями через `asyncpg`.  
🔹 **Performance Tracking** — встроенная Middleware для логирования медленных запросов.  
🔹 **Smart Validation** — строгая проверка данных через Pydantic (email, возраст, пустые строки).  
🔹 **Lifespan Management** — корректное открытие и закрытие ресурсов БД.

---

## 🛠 Установка и запуск

1️⃣ **Клонируйте репозиторий:**
```bash
git clone <url_вашего_репозитория>
cd <папка_проекта>
```

2️⃣ **Настройте переменные окружения:**
Создайте файл `.env` в корневой директории:
```env
DATABASE_URL=postgresql://postgres:password@localhost:5432/your_db
ADMIN_PASSWORD=top_secret_pass
```

3️⃣ **Установите зависимости:**
```bash
pip install -r requirements.txt
```

4️⃣ **Запустите сервер:**
```bash
uvicorn main:app --reload
```

---

## 🔌 API Эндпоинты

### 👥 Пользователи

| Метод | Путь | Описание |
| :--- | :--- | :--- |
| `GET` | `/` | Статус сервера 🟢 |
| `GET` | `/users` | Список всех пользователей |
| `POST` | `/add_user` | Регистрация нового пользователя |
| `DELETE` | `/clear` | Очистка БД (только для админа) ⚠️ |

---

## 🏗 Структура проекта

```text
.
├── 📄 main.py      # Инициализация FastAPI и роутинг
├── 📄 db.py        # Логика БД и SQL запросы
├── 📄 schemas.py   # Pydantic модели (схемы)
├── 📄 .env         # Конфиденциальные данные
└── 📄 requirements.txt
```

---

## 🛡 Схемы данных

### UserDataForm (POST /add_user)
```json
{
  "name": "Ivan",
  "age": 25,
  "email": "ivan@example.com"
}
```

### PasswordForm (DELETE /clear)
```json
{
  "password": "your_admin_password"
}
```

---

## 📝 Документация
После запуска доступна по ссылкам:
* **Swagger UI**: [http://127.0.0](http://127.0.0)
* **ReDoc**: [http://127.0.0](http://127.0.0)

---
<p align="center">Made with ❤️ for clean code</p>
