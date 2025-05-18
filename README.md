   ## Запуск тестов

   Установите зависимости:
   pip install -r requirements.txt

   Запустите тесты с покрытием:
   coverage run -m pytest tests/
   coverage report
   coverage html

   ## Нагрузочное тестирование

   locust -f tests/locustfile.py
