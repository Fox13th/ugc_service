import logging
import random
import time

from clickhouse_driver import Client
import uuid


def get_random_param():
    rand_user_id = str(uuid.uuid4())
    rand_movie_id = str(uuid.uuid4())
    rand_num = random.randint(0, 10000000)
    return rand_user_id, rand_movie_id, rand_num


def generate_data(num: int) -> str:
    list_data = []
    for i in range(num):
        list_rand = get_random_param()
        list_data.append(f"({i}, '{list_rand[0]}', '{list_rand[1]}', {list_rand[2]})")
    return ', '.join(list_data)


def insert_data(num: int, chunk: int):
    i_num = 0
    gen_time_data = 0
    while i_num < num:
        start_time = time.time()
        ins_data = generate_data(chunk)
        end_time = time.time()
        gen_time_data += end_time - start_time

        client.execute(f"INSERT INTO default.test (id, user_id, movie_id, frame) VALUES {ins_data}")

        i_num += 1000
    return gen_time_data


def read_data():
    return client.execute('SELECT frame, count(*) number FROM default.test GROUP BY frame')


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")

    client = Client('127.0.0.1')

    start_insert_time = time.time()
    sum_gen_time_data = insert_data(10000000, 1000)
    end_insert_time = time.time()
    logging.info(f'Скорость вставки данных: {end_insert_time - start_insert_time - sum_gen_time_data}')

    time.sleep(1)

    start_read_time = time.time()
    select_db = read_data()
    end_read_time = time.time()
    logging.info(f'Скорость чтения данных: {end_read_time - start_read_time}')
