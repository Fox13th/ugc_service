# Сервис сбора статистики пользователей UGC_Service

# Запуск проекта:
1) В корне проекта лежит файл `.env.example`. Необходимо создать файл `.env` и указать в нем переменные окружения. Для тестового запуска можно использовать значения из `.env.example`.

# Cхема сервиса:



# Результаты тестов хранилищ:
1) Vertica:
   Загрузка множества записей в данное хранилище весьма медленное.

   Тесты были проведены на компьютере с характеристиками:
   - OS Windows 10;
   - Процессор AMD Ryzen 7 3700X;
   - 16 GB ОЗУ.

   Для работы хранилища использовался docker контейнер `docker run -p 5433:5433 jbfavre/vertica:latest`
    
   Вставка 10000 данных:
      [2024-07-07 22:59:14,974] [INFO] Time taken to write: 50.221513748168945 sec
      [2024-07-07 22:59:15,063] [INFO] Time taken to read 10000 rows: 0.06251978874206543 sec
      [2024-07-07 22:59:15,063] [INFO] Time taken to update 100 rows: 0.016718149185180664 sec

   Вставка и чтение данных при уже имеющихся данных:
      [2024-07-07 23:09:24,497] [INFO] Time taken to write: 49.11543560028076 sec
      [2024-07-07 23:09:24,645] [INFO] Time taken to read 20000 rows: 0.1271681785583496 sec
      [2024-07-07 23:09:24,645] [INFO] Time taken to update 100 rows: 0.016921043395996094 sec

   Работа с хранилищем при постоянной нагрузке:
      [2024-07-07 23:13:26,323] [INFO] Time taken to write: 66.41842532157898 sec
      [2024-07-07 23:13:26,551] [INFO] Time taken to read 30260 rows: 0.20050644874572754 sec
      [2024-07-07 23:13:26,551] [INFO] Time taken to update 100 rows: 0.023291826248168945 sec
