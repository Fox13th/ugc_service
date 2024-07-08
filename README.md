# Сервис сбора статистики пользователей UGC_Service

# Запуск проекта:
1) В корне проекта лежит файл `.env.example`. Необходимо создать файл `.env` и указать в нем переменные окружения. Для тестового запуска можно использовать значения из `.env.example`.

# Cхема сервиса:

![Image alt](https://github.com/Fox13th/ugc_service/blob/dev/scheme.png)

# Результаты тестов хранилищ:
В результате проведенных тестов между <b>ClickHouse</b> и <b>Vertica</b> были сделаны следующие выводы:

При вставки множества записей <b>ClickHouse</b> показало себя более эффективным хранилищем, которое позволяет осуществить запись 10000000 данных за 50,134 (сек), в отличие от <b>Vertica</b>, которая при прочих равных условиях выполняет запись 10000 данных за 33,6 (сек). Скорость чтения имеет незначительные отличия. При нагрузке <b>ClickHouse</b> показывает тоже неплохой результат - скорость вставки 10000 данных за 0.0489 (сек), чтения 10993452 данных за 14.66 (сек), выполнение агрегирующих запросов за 2.046 (сек).

Тесты были проведены на компьютере с характеристиками:
   - OS Windows 10;
   - Процессор Intel Core i7 9700k;
   - 64 GB ОЗУ.

*В зависимости от характеристик компьютера значения могут меняться. Скрипты генерации данных и тестирования хранилищ представлены в папке `tests_db` 
    
