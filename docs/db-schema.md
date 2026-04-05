# Структура БД (v1)

Ниже — нормализованная схема для MVP веб‑приложения каталога фарфоровых молочников.

## 1) users

| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | BIGSERIAL | PK | Идентификатор пользователя |
| name | VARCHAR(120) | NOT NULL | Отображаемое имя |
| email | VARCHAR(255) | NOT NULL, UNIQUE | Email для входа |
| password_hash | VARCHAR(255) | NOT NULL | Хэш пароля |
| role_id | BIGINT | FK -> roles.id, NOT NULL | Роль |
| avatar_path | VARCHAR(500) | NULL | Путь к аватару |
| bio | TEXT | NULL | Краткая информация |
| visibility_default | VARCHAR(20) | NOT NULL, DEFAULT 'registered' | Видимость по умолчанию для новых карточек |
| is_active | BOOLEAN | NOT NULL, DEFAULT TRUE | Активность учетной записи |
| email_verified_at | TIMESTAMPTZ | NULL | Дата подтверждения email |
| last_login_at | TIMESTAMPTZ | NULL | Последний вход |
| created_at | TIMESTAMPTZ | NOT NULL | Дата создания |
| updated_at | TIMESTAMPTZ | NOT NULL | Дата изменения |
| deleted_at | TIMESTAMPTZ | NULL | Soft delete |

**Индексы:** `UNIQUE(email)`, `INDEX(role_id)`, `INDEX(is_active)`.

---

## 2) roles

| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | BIGSERIAL | PK | Идентификатор роли |
| code | VARCHAR(50) | NOT NULL, UNIQUE | `guest`, `user`, `admin` |
| name | VARCHAR(120) | NOT NULL | Название роли |
| created_at | TIMESTAMPTZ | NOT NULL | Дата создания |
| updated_at | TIMESTAMPTZ | NOT NULL | Дата изменения |

---

## 3) items

| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | BIGSERIAL | PK | Идентификатор предмета |
| user_id | BIGINT | FK -> users.id, NOT NULL | Владелец |
| title | VARCHAR(255) | NULL | Название предмета |
| manufacturer_id | BIGINT | FK -> manufacturers.id, NULL | Производитель |
| sculptor_id | BIGINT | FK -> sculptors.id, NULL | Скульптор |
| artist_id | BIGINT | FK -> artists.id, NULL | Художник |
| form_id | BIGINT | FK -> forms.id, NULL | Форма |
| painting_id | BIGINT | FK -> paintings.id, NULL | Роспись |
| material_id | BIGINT | FK -> materials.id, NULL | Материал |
| country_id | BIGINT | FK -> countries.id, NULL | Страна |
| factory_name | VARCHAR(255) | NULL | Фабрика/завод (свободный ввод) |
| category | VARCHAR(120) | NULL | Категория предмета |
| creation_year | SMALLINT | NULL | Год создания |
| creation_period | VARCHAR(120) | NULL | Период создания |
| production_period | VARCHAR(120) | NULL | Период производства |
| dimensions | VARCHAR(120) | NULL | Общие размеры |
| height_cm | NUMERIC(6,2) | NULL | Высота (см) |
| volume_ml | INTEGER | NULL | Объем (мл) |
| weight_g | INTEGER | NULL | Вес (г) |
| condition_text | TEXT | NULL | Состояние |
| defects | TEXT | NULL | Дефекты |
| hallmark | BOOLEAN | NOT NULL, DEFAULT FALSE | Есть ли клеймо |
| hallmark_description | TEXT | NULL | Описание клейма |
| source | VARCHAR(255) | NULL | Происхождение предмета |
| acquired_at | DATE | NULL | Дата поступления в коллекцию |
| comments | TEXT | NULL | Комментарии |
| owner_notes | TEXT | NULL | Примечания владельца |
| visibility_status | VARCHAR(20) | NOT NULL, DEFAULT 'registered' | `private`, `registered`, `public` |
| publication_status | VARCHAR(20) | NOT NULL, DEFAULT 'draft' | `draft`, `published`, `hidden` |
| created_at | TIMESTAMPTZ | NOT NULL | Дата создания |
| updated_at | TIMESTAMPTZ | NOT NULL | Дата изменения |
| deleted_at | TIMESTAMPTZ | NULL | Soft delete |

**Индексы:**
- `INDEX(user_id)`
- `INDEX(publication_status, visibility_status)`
- `INDEX(manufacturer_id, sculptor_id, artist_id)`
- `INDEX(form_id, painting_id, creation_year)`
- `GIN(to_tsvector('simple', coalesce(title,'') || ' ' || coalesce(comments,'')))` для полнотекста.

---

## 4) photos

| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | BIGSERIAL | PK | Идентификатор фото |
| item_id | BIGINT | FK -> items.id, NOT NULL | Связанный предмет |
| file_path | VARCHAR(500) | NOT NULL | Оригинал |
| preview_path | VARCHAR(500) | NULL | Превью |
| width | INTEGER | NULL | Ширина оригинала |
| height | INTEGER | NULL | Высота оригинала |
| mime_type | VARCHAR(100) | NOT NULL | MIME-тип |
| file_size_bytes | BIGINT | NOT NULL | Размер файла |
| is_main | BOOLEAN | NOT NULL, DEFAULT FALSE | Главное фото |
| sort_order | INTEGER | NOT NULL, DEFAULT 0 | Порядок сортировки |
| created_at | TIMESTAMPTZ | NOT NULL | Дата загрузки |
| deleted_at | TIMESTAMPTZ | NULL | Soft delete |

**Индексы:** `INDEX(item_id)`, `INDEX(item_id, is_main)`, `INDEX(item_id, sort_order)`.

---

## 5) Справочники

Для всех справочников действует единый паттерн: `id`, `name` (или `full_name`), `description`, `created_at`, `updated_at`, `deleted_at`.

- manufacturers (`country_id` nullable FK -> countries.id)
- sculptors (`full_name`)
- artists (`full_name`)
- forms
- paintings
- materials
- countries

**Требование антидублей:** `UNIQUE(lower(name))` / `UNIQUE(lower(full_name))`.

---

## 6) Администрирование и аудит

### admin_actions

| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | BIGSERIAL | PK | Идентификатор события |
| admin_id | BIGINT | FK -> users.id, NOT NULL | Администратор |
| action | VARCHAR(100) | NOT NULL | Тип действия |
| entity_type | VARCHAR(50) | NOT NULL | Сущность (`item`, `user`, `photo`, `dictionary`) |
| entity_id | BIGINT | NULL | ID сущности |
| payload | JSONB | NULL | Детали изменений |
| created_at | TIMESTAMPTZ | NOT NULL | Дата события |

### auth_logs

| Поле | Тип | Ограничения | Описание |
|---|---|---|---|
| id | BIGSERIAL | PK | Идентификатор события входа |
| user_id | BIGINT | FK -> users.id, NULL | Пользователь (если найден) |
| email | VARCHAR(255) | NULL | Email из формы |
| event_type | VARCHAR(30) | NOT NULL | `login_success`, `login_failed`, `logout`, `password_reset` |
| ip_address | INET | NULL | IP |
| user_agent | TEXT | NULL | User-Agent |
| created_at | TIMESTAMPTZ | NOT NULL | Дата события |

---

## 7) Кардинальности

- `roles (1) -> (N) users`
- `users (1) -> (N) items`
- `items (1) -> (N) photos`
- каждый справочник `(1) -> (N) items`

---

## 8) Рекомендации по миграциям

1. Создать справочники и роли.
2. Создать `users`, затем `items`, затем `photos`.
3. Добавить ограничения уникальности и индексы после первичной загрузки данных.
4. Добавить полнотекстовый индекс и периодические reindex/vacuum задачи.
