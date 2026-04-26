# Каталог фарфоровых молочников

Production-ready Flask-проект каталога коллекции фарфоровых молочников.

## Единая структура проекта (готово к выгрузке на хостинг)

```text
farfor/
  app/                  # Flask приложение (blueprints, models, forms, services, templates, static)
  deploy/               # production-конфиги (gunicorn/nginx/systemd)
  scripts/              # утилиты сборки релиза
  tests/                # pytest сценарии
  manage.py             # Flask CLI (init-db / seed-db)
  wsgi.py               # entrypoint для gunicorn/uWSGI
  requirements.txt
  .env.example
  Dockerfile
  docker-compose.yml
```

## Возможности
- Регистрация/логин/профиль.
- CRUD карточек предметов + множественная загрузка фото.
- Каталог с поиском, фильтрами, сортировкой, пагинацией.
- RBAC: пользователь/админ, защита чувствительных операций.
- Управление справочниками и просмотр всех пользователей/карточек в админке.
- Обработчики ошибок 403/404/500.

## Локальный запуск
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
flask --app manage.py init-db
flask --app manage.py seed-db
flask --app manage.py run --debug
```

## Подготовка релиза для выгрузки на хостинг

1. Создать архив релиза:
```bash
./scripts/build_release.sh
```
2. Получится `farfor_release.tar.gz` — его можно загружать на сервер.

## Деплой на Linux VPS (Nginx + Gunicorn + systemd)

### 1) На сервере
```bash
sudo mkdir -p /var/www/farfor
sudo tar -xzf farfor_release.tar.gz -C /var/www/farfor
cd /var/www/farfor
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
```

### 2) Инициализация БД
```bash
flask --app manage.py init-db
flask --app manage.py seed-db
```

### 3) systemd
```bash
sudo cp deploy/farfor.service /etc/systemd/system/farfor.service
sudo systemctl daemon-reload
sudo systemctl enable --now farfor
sudo systemctl status farfor
```

### 4) Nginx
```bash
sudo cp deploy/nginx.conf /etc/nginx/sites-available/farfor
sudo ln -s /etc/nginx/sites-available/farfor /etc/nginx/sites-enabled/farfor
sudo nginx -t
sudo systemctl reload nginx
```

## Docker запуск
```bash
docker compose up --build -d
```

## Тесты
```bash
pytest
```

---

## Android MVP (Flutter + FastAPI)

В репозиторий добавлен отдельный MVP-стек под мобильное приложение:

- `mvp_mobile/` — Flutter-клиент (Android-first), полностью русскоязычный интерфейс.
- `mvp_backend/` — FastAPI API с JWT, PostgreSQL и загрузкой фотографий в S3-compatible storage (или локальный fallback).

### Что уже закрыто в MVP
- Регистрация и вход.
- Личный кабинет и личная коллекция пользователя.
- Добавление предмета с фотографией с камеры или несколькими фото из галереи.
- Атрибуты карточки: производитель, автор формы, автор росписи, название формы, название росписи, год, период, материал, состояние, размер, место, комментарий.
- Редактирование и удаление предметов через API.
- Поиск и фильтры через API.
- Публичность коллекции и отдельных предметов.
- Просмотр публичных предметов и публичных коллекций других пользователей.

### Быстрый запуск нового стека

Backend:
```bash
cd mvp_backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Flutter:
```bash
cd mvp_mobile
flutter pub get
flutter run
```
