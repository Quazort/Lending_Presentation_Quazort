## Lending Quazort Backend
Backend-система для обработки комментариев с AI-аналитикой, email-уведомлениями и автоматизированным хранением данных.

1. Стек технологий
- Язык: Python 3.12
- Фреймворк: FastAPI (асинхронность, высокая производительность)
- База данных: SQLite + SQLAlchemy (Async)
- AI: Интеграция LLM для анализа тональности и генерации ответов
- Email: aiosmtplib для асинхронной отправки писем


2. Архитектура
Проект построен по слоистой структуре:
- core/ - конфигурация, логгирование, база данных.
- repositories/ - слой работы с данными (AI, Mail, DB).
- models/ - схемы данных (SQLAlchemy).
- services/ - работа с бизнес логикой

3. Инструкция по запуску

Требования:
- Docker и Docker Compose

Перед началом работы скопируйте этот репозиторий к себе на локаль:

```commandline
git clone https://github.com/Quazort/Lending_Presentation_Quazort.git
```

Дальше в корне проекта создайте файл .env в который пропишите следующие переменные
- AI_MODEL="модель"
- AI_KEY="ваш Api key от модели"
- DATABASE_URL="sqlite+aiosqlite:///./database.sqlite3"
- BASE_API_AI="юрл подключения к дипсику"
- SMTP_USER="xxxxx@mail.ru"
- ADMIN_EMAIL="xxxxx@mail.ru"
- SMTP_HOST="smtp.mail.ru"
- SMTP_PORT="465"
- SMTP_PASSWORD="пароль от smtp"
- AI_SYSTEM_PROMPT="Ты — автоматический ассистент-автоответчик...."

Дальше запустите докер локально и введите в терминале в корне проекта

```commandline
docker-compose up --build
```

Приложение будет доступно по адресу http://localhost:8000.

4. Реализация API

- /api/contact - ручка для отправки почты 
- /api/health - ручка для проверки жизни сервиса
- /api/metrics - ручка для получения метрик 


5. AI-интеграция:

- Инструмент: LLM-клиент для обработки входящего текста.
- Автоматический ответ ИИ

6. Что сделано с помощью AI:

- фронтенд
- настройка почты, проблемы с SMTP

7. Хранение данных:

Использована бд SQLlite
