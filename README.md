# Приложение для коллекционеров фарфоровых молочников

## Описание

Android-приложение для ведения коллекции фарфоровых молочников и сливочников. Позволяет добавлять предметы с фотографиями, заполнять атрибуты, управлять видимостью и просматривать публичные коллекции других пользователей.

## Структура проекта

```
/workspace
├── backend/                 # FastAPI сервер
│   ├── main.py             # Основной файл API
│   └── requirements.txt    # Python зависимости
└── mobile/                 # Flutter приложение
    ├── lib/
    │   ├── main.dart       # Точка входа
    │   ├── models/         # Модели данных
    │   ├── screens/        # Экраны приложения
    │   ├── services/       # Сервисы (API, auth)
    │   └── widgets/        # Переиспользуемые виджеты
    └── pubspec.yaml        # Flutter зависимости
```

## Быстрый старт

### Backend

```bash
cd /workspace/backend
pip install -r requirements.txt
python main.py
```

Сервер запустится на `http://localhost:8000`

### Mobile

```bash
cd /workspace/mobile
flutter pub get
flutter run
```

## API Endpoints

### Аутентификация
- `POST /auth/register` - Регистрация нового пользователя
- `POST /auth/login` - Вход в систему
- `GET /auth/me` - Получение текущего пользователя

### Предметы коллекции
- `GET /items` - Список предметов (с фильтрами)
- `GET /items/{id}` - Детали предмета
- `POST /items` - Создать предмет (с фото)
- `PUT /items/{id}` - Обновить предмет
- `DELETE /items/{id}` - Удалить предмет
- `DELETE /items/{id}/photos/{photo_id}` - Удалить фото

### Публичный доступ
- `GET /public/items` - Публичные предметы (без авторизации)

## Функционал MVP

### Реализовано:
✅ Регистрация и вход (JWT)
✅ Личный кабинет пользователя
✅ Добавление предмета с фото (камера/галерея)
✅ Заполнение атрибутов:
  - Производитель
  - Автор формы
  - Автор росписи
  - Название формы
  - Название росписи
  - Год выпуска
  - Период
  - Материал
  - Состояние
  - Размер
  - Место нахождения/приобретения
  - Комментарий
✅ Редактирование предметов
✅ Удаление предметов
✅ Поиск и фильтрация
✅ Переключение видимости (публичный/приватный)
✅ Просмотр своей коллекции
✅ Просмотр всех коллекций
✅ Просмотр публичных коллекций (без авторизации)
✅ Галерея фотографий с зумом

### Не реализовано (MVP):
❌ AI-распознавание предметов
❌ Маркетплейс
❌ Чаты между пользователями
❌ Оплата

## Дизайн

- Спокойный, музейный стиль
- Акцент на фотографиях предметов
- Теплая коричневая цветовая гамма
- Material Design 3

## Технологии

### Backend
- FastAPI (Python)
- SQLite (для MVP, легко заменяется на PostgreSQL)
- JWT авторизация
- Локальное хранение файлов (легко заменяется на S3)

### Mobile
- Flutter (Dart)
- Provider (state management)
- Image Picker (камера/галерея)
- Photo View (зум фотографий)
- HTTP/Dio (сетевые запросы)

## Настройка подключения

В файле `mobile/lib/services/api_service.dart` измените `baseUrl` на адрес вашего сервера:

```dart
static const String baseUrl = 'http://your-server-ip:8000';
```

## Развертывание

### Production Backend

1. Замените SQLite на PostgreSQL
2. Настройте S3-compatible storage для фото
3. Измените `SECRET_KEY` в `main.py`
4. Настройте HTTPS
5. Используйте переменные окружения для конфиденциальных данных

### Production Mobile

1. Настройте signing для Android
2. Измените `baseUrl` на production сервер
3. Соберите релизную версию:
   ```bash
   flutter build apk --release
   flutter build appbundle --release
   ```

## База данных

Для перехода на PostgreSQL обновите `get_db()` в `backend/main.py`:

```python
import psycopg2

def get_db():
    conn = psycopg2.connect(
        host=os.getenv('DB_HOST'),
        database=os.getenv('DB_NAME'),
        user=os.getenv('DB_USER'),
        password=os.getenv('DB_PASSWORD')
    )
    # ... остальной код
```

## Лицензия

MIT
