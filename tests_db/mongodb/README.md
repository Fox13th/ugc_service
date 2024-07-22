# Как запустить тест MongoDB

1) В консоле ввести команду `docker-compose up`. В результате запустится образ mongo.
2) Произвети запуск скрипта `python mongo.py <количество записей> <количество пользователей> <количество фильмов>`.
3) Результатом работы скрипта будет загруженные данные (в указанном количестве) и время работы 3-х агрегирующих запросов:
- время вставки лайков;
- средняя пользовательская оценка фильма;
- количество лайков или дизлайков;
- список понравившихся пользователю фильмов.