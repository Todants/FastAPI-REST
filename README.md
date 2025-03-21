# REST API для справочника Организаций, Зданий и Деятельностей

## Описание проекта

Проект представляет собой REST API приложение для управления справочником организаций, зданий и видов деятельности. API позволяет:
- Управлять организациями, зданиями и видами деятельности.
- Искать организации по различным критериям (по зданию, виду деятельности, местоположению, названию).
- Ограничивать уровень вложенности видов деятельности до 3 уровней.

### Основные сущности:
1. **Организация**:
   - Название.
   - Номера телефонов (может быть несколько).
   - Здание (одно конкретное здание).
   - Виды деятельности (может быть несколько).

2. **Здание**:
   - Адрес.
   - Географические координаты (широта и долгота).

3. **Деятельность**:
   - Название.
   - Древовидная структура (вложенность до 3 уровней).

---

## Технологический стек
- **FastAPI**: Фреймворк для создания API.
- **Pydantic**: Валидация данных.
- **SQLAlchemy**: ORM для работы с базой данных.
- **Alembic**: Управление миграциями базы данных.
- **Docker**: Контейнеризация приложения.
- **Swagger UI**: Документация API.

---

## Установка и запуск

### 1. Клонируйте репозиторий
```bash
git clone https://github.com/Todants/FastAPI-REST.git
cd FastAPI-REST-main
```

### 2. Запустите приложение с помощью Docker

Убедитесь, что у вас установлен Docker и Docker Compose.

1. Соберите и запустите контейнеры:
   ```bash
   docker-compose up --build
   ```
2. Приложение будет доступно по адресу:
- **API**: `http://localhost:8000`
- **Swagger UI**: `http://localhost:8000/docs`

---

## Тестовые данные
При запуске приложения база данных автоматически заполняется тестовыми данными:
- **Деятельности**:
  - Еда
    - Мясная продукция
    - Молочная продукция
  - Автомобили
    - Грузовые
    - Легковые
    - Запчасти
    - Аксессуары
- **Здания**:
  - 3 здания, два из которых находятся рядом по координатам.
- **Организации**:
  - 4 организации, связанные с разными видами деятельности.

---

## Документация API
Документация API доступна через Swagger UI:
- **Swagger UI**: `http://localhost:8000/docs`
- **Redoc**: `http://localhost:8000/redoc`

---
