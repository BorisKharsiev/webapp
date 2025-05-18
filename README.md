# Task Manager API

## Установка зависимостей

```bash
pip install -r requirements.txt
```

## Запуск сервера

```bash
python mainn.py
```

## Открытие Swagger UI

После запуска сервера откройте в браузере:
```
http://127.0.0.1:8000/docs
```

## Запуск тестов

### Unit и API тесты

```bash
pytest tests/
```

### Проверка покрытия кода

```bash
coverage run -m pytest tests/
coverage report
coverage html
```

### Нагрузочное тестирование

```bash
locust -f tests/locustfile.py
```

После запуска Locust откройте в браузере:
```
http://localhost:8089
```

## Примечания
- Для работы кэширования требуется установленный и запущенный Redis.
- База данных создаётся автоматически при первом запуске.
- Все тесты находятся в папке `tests/`.
