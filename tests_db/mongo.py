import random
import time
import uuid
from typing import Any

from pymongo import MongoClient
from pymongo.collection import Collection


def get_random(list_user_id: list, list_movie_id: list) -> list:
    random_user = random.choice(list_user_id)
    random_movie = random.choice(list_movie_id)
    rand_like = random.randint(0, 1)
    return [random_user, random_movie, rand_like]


def insert_document(*, collection: Collection, num: int) -> Any:
    i_num = 0
    chunk = 1000
    if num < chunk:
        chunk = num

    random_user_id = [str(uuid.uuid4()) for i in range(100000)]
    random_movie_id = [str(uuid.uuid4()) for i in range(60000)]

    while i_num < num:
        try:
            list_data = []
            for i in range(chunk):
                data_id = get_random(random_user_id, random_movie_id)
                data = {'movie_id': f'{data_id[1]}', 'user_id': f'{data_id[0]}', 'score': data_id[2]}
                list_data.append(data)

            collection.insert_many(list_data)

            i_num += chunk
        except IndexError:
            break


def find(*, collection: Collection):
    pipeline = [
        #{'$match': {'subgroup': 'movie_id'}},
        {'$group': {'_id': '$movie_id', 'total_score': {'$avg': '$score'}}}
    ]

    return collection.aggregate(pipeline)


def delete_document(*, collection: Collection, condition: dict):
    collection.delete_one(condition)


if __name__ == '__main__':
    # Создание клиента
    # Берем из расчёта 60000 фильмов на 100000 пользователей

    client = MongoClient('127.0.0.1', 27017)

    # Подключение к базе данных
    db = client['UsersDB']

    start_time = time.time()
    insert_document(collection=db.users, num=6000000000)
    end_time = time.time()

    print(f'Время вставки лайков: {end_time - start_time}')

    start_time = time.time()
    res = find(collection=db.users)
    end_time = time.time()

    for row in res:
        print(row)

    print(f'Время чтения лайков: {end_time - start_time}')


