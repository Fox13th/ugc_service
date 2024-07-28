import logging
import random
import sys
import uuid
from contextlib import closing

import psycopg2
from psycopg2.extras import execute_values, DictCursor
import time


def get_random(list_user_id: list, list_movie_id: list) -> list:
    random_user = random.choice(list_user_id)
    random_movie = random.choice(list_movie_id)
    rand_like = random.randint(0, 1)
    return [random_user, random_movie, rand_like]


def create_table():
    cur.execute("""
                    CREATE TABLE IF NOT EXISTS test_table (
                        id SERIAL PRIMARY KEY,
                        user_id TEXT,
                        movie_id TEXT,
                        score INT
                    )
                    """)
    pg_conn.commit()


def write_data(num: int):
    start_time = time.time()

    i_num = 0
    chunk = 1000
    if num < chunk:
        chunk = num

    random_user_id = [str(uuid.uuid4()) for i in range(int(sys.argv[5]))]  # 100000
    random_movie_id = [str(uuid.uuid4()) for i in range(int(sys.argv[6]))]  # 60000

    while i_num < num:
        try:
            list_data = []
            for i in range(chunk):
                data_id = get_random(random_user_id, random_movie_id)
                data_to_insert = [data_id[0], data_id[1], data_id[2]]
                list_data.append(data_to_insert)

            execute_values(cur, "INSERT INTO test_table (user_id, movie_id, score) VALUES %s", list_data)
            pg_conn.commit()
            i_num += 1000
        except IndexError:
            break
    end_time = time.time()

    logging.info(f"Total time for inserting {num} rows in batches of {chunk}: {end_time - start_time} seconds")
    return random_user_id[0], random_movie_id[1]


def read_data(query: str):
    start_time = time.time()
    cur.execute(query)
    rows = cur.fetchall()
    end_time = time.time()
    logging.info(f"Total time for reading {len(rows)} rows: {end_time - start_time} seconds")


def drop_table():
    cur.execute("DROP TABLE test_table")
    pg_conn.commit()


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")

    dsl = {
        'dbname': sys.argv[1],
        'user': sys.argv[2],
        'password': sys.argv[3],
        'host': '127.0.0.1',
        'port': 5432,
    }

    with closing(psycopg2.connect(**dsl, cursor_factory=DictCursor)) as pg_conn:
        cur = pg_conn.cursor()
        create_table()
        u_id, m_id = write_data(int(sys.argv[4]))
        read_data("SELECT * FROM test_table")
        read_data(
            f"SELECT movie_id, AVG(score) FROM test_table Where movie_id='{m_id}' GROUP BY movie_id;")
        read_data(
            f"SELECT Count(*) FROM test_table Where user_id='{u_id}' and score=1 GROUP BY user_id;")
        read_data(f"SELECT movie_id FROM test_table Where user_id='{u_id}' and score=1;")
        drop_table()
