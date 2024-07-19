import logging
import random
import sys
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

    random_user_id = [str(uuid.uuid4()) for i in range(int(sys.argv[2]))] # 100000
    random_movie_id = [str(uuid.uuid4()) for i in range(int(sys.argv[3]))] # 60000

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
    return random_movie_id, random_user_id


def find(*, collection: Collection, id_data: dict, action: str):
    pipeline = [
        {'$match': id_data},
        {'$group': {'_id': f'$movie_id', 'total_score': {f'${action}': '$score'}}}
    ]

    return collection.aggregate(pipeline)


def delete_document(*, collection: Collection, condition: dict):
    collection.delete_one(condition)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")

    client = MongoClient('127.0.0.1', 27017)

    db = client['UsersDB']

    start_time = time.time()
    movie_id, user_id = insert_document(collection=db.users, num=int(sys.argv[1]))
    end_time = time.time()
    rand_movie_id = random.choice(movie_id)
    rand_user_id = random.choice(user_id)

    logging.info(f'Время вставки лайков: {end_time - start_time}')

    start_time = time.time()
    data = {'movie_id': rand_movie_id}
    res = find(collection=db.users, id_data=data, action='avg')
    end_time = time.time()
    for row in res:
        logging.info(row)
    logging.info(f'Cредняя пользовательская оценка фильма: {end_time - start_time}')

    start_time = time.time()
    res = find(collection=db.users, id_data=data, action='sum')
    end_time = time.time()
    for row in res:
        logging.info(row)
    logging.info(f'Количество лайков или дизлайков: {end_time - start_time}')

    start_time = time.time()
    data = {'$and': [{'user_id': rand_user_id}, {'score': 1}]}
    res = find(collection=db.users, id_data=data, action='sum')
    end_time = time.time()
    for row in res:
        logging.info(row)
    logging.info(f'Cписок понравившихся пользователю фильмов: {end_time - start_time}')

