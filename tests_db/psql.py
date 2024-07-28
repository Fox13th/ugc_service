import os
import sys
import uuid
from contextlib import closing

import psycopg2
from psycopg2.extras import execute_values, DictCursor
import time


def create_table():
    cur.execute("""
                    CREATE TABLE IF NOT EXISTS test_table (
                        id SERIAL PRIMARY KEY,
                        data TEXT
                    )
                    """)
    pg_conn.commit()


def write_data(num: int):
    data_to_insert = [(f'data_{i}',) for i in range(1, 1000000)]
    batch_size = 1000
    total_rows = len(data_to_insert)
    num_batches = total_rows // batch_size

    start_time = time.time()

    i_num = 0
    chunk = 1000
    if num < chunk:
        chunk = num

    #random_user_id = [str(uuid.uuid4()) for i in range(int(sys.argv[2]))]  # 100000
    #random_movie_id = [str(uuid.uuid4()) for i in range(int(sys.argv[3]))]  # 60000

    while i_num < num:
        try:
            list_data = []
            #for i in range(chunk):
                #data_id = get_random(random_user_id, random_movie_id)
                #data = {'movie_id': f'{data_id[1]}', 'user_id': f'{data_id[0]}', 'score': data_id[2]}
            for i in range(1, 1000):
                list_data.append(data_to_insert[i])

            execute_values(cur, "INSERT INTO test_table (data) VALUES %s", list_data)
            pg_conn.commit()
            i_num += 1000
            print(i_num)
        except IndexError:
            break
    end_time = time.time()

    print(f"Total time for inserting {total_rows} rows in batches of {batch_size}: {end_time - start_time} seconds")
    print(f"Average time per {batch_size} rows: {(end_time - start_time) / num_batches} seconds")


def read_data():
    start_time = time.time()
    cur.execute("SELECT * FROM test_table")
    rows = cur.fetchall()
    end_time = time.time()
    print(f"Total time for reading {len(rows)} rows: {end_time - start_time} seconds")


if __name__ == '__main__':
    dsl = {
        'dbname': 'movies_database',
        'user': 'postgres',
        'password': '123qwe',
        'host': '127.0.0.1',
        'port': 5432,
    }

    with closing(psycopg2.connect(**dsl, cursor_factory=DictCursor)) as pg_conn:
        cur = pg_conn.cursor()
        create_table()
        write_data(100000)
        read_data()
