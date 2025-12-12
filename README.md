# To-Do System

![CI/CD Status](https://github.com/MrDickenson/Web_project/actions/workflows/ci.yml/badge.svg)

## Локальний запуск

### Без Docker
1. Встановіть залежності: `pip install -r requirements.txt`
2. Запустіть сервер: `python src/app.py`
3. Відкрийте у браузері: `http://localhost:3000`

### Через Docker
1. Збірка: `docker build -t todo-app .`
2. Запуск: `docker run -p 3000:3000 todo-app`

## CI/CD Delivery
У цьому проєкті реалізовано підхід **Delivery via Artifacts**:
1. При кожному пуші проходять автотести (`pytest`) та перевірка коду (`flake8`).
2. Після успішних тестів збирається Docker-образ застосунку.
3. Образ архівується та доступний для завантаження у вкладці "Actions" -> "Artifacts" як файл `todo-app-docker-image`.