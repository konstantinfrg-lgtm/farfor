# Farfor MVP Backend (FastAPI)

API для мобильного Android-приложения коллекционеров фарфоровых молочников/сливочников.

## Что реализовано (MVP)
- Регистрация и вход (JWT).
- Личная коллекция пользователя.
- CRUD карточек предметов.
- Множественная загрузка фото (S3-compatible или локальное хранилище).
- Поиск/фильтры по личной коллекции.
- Публичность коллекции и отдельных предметов.
- Публичный просмотр чужих коллекций.

## Запуск
```bash
cd mvp_backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

## ENV
- `DATABASE_URL`
- `SECRET_KEY`
- `S3_ENDPOINT_URL`, `S3_ACCESS_KEY_ID`, `S3_SECRET_ACCESS_KEY`, `S3_BUCKET`
- `MEDIA_BASE_URL` (для локального fallback)
