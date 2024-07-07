import time
import uuid
import logging

import vertica_python


def get_random():
    random_user_id = str(uuid.uuid4())
    random_movie_id = str(uuid.uuid4())
    return random_user_id, random_movie_id


def create_table(curs):
    curs.execute("""
    CREATE TABLE views (
        id IDENTITY,
        user_id VARCHAR(256) NOT NULL,
        movie_id VARCHAR(256) NOT NULL,
        viewed_frame INTEGER NOT NULL
    );
    """)


def drop_table(curs):
    curs.execute("""DROP TABLE views;""")


def write_speed_test(num: int):
    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()

        try:
            create_table(cursor)

            start_time = time.time()

            i_num = 0

            while i_num < num:
                try:
                    for i in range(1000):
                        data_id = get_random()
                        cursor.execute(
                            f"INSERT INTO views (user_id, movie_id, viewed_frame) VALUES ('{data_id[0]}', "
                            f"'{data_id[1]}', "
                            f"{i})")
                    i_num += 1000
                except IndexError:
                    break

            end_time = time.time()

            cursor.close()

        except Exception:
            drop_table(cursor)
            exit(1)

        return end_time - start_time


def read_speed_test():
    with vertica_python.connect(**connection_info) as connection:
        cursor = connection.cursor()
        try:
            start_time = time.time()

            cursor.execute("SELECT * FROM views;")
            rows = cursor.fetchall()

            end_time = time.time()

            rand_id = get_random()

            start_exec = time.time()

            cursor.execute(f"UPDATE views SET movie_id = '{rand_id[1]}' WHERE viewed_frame < 1000000")

            end_exec = time.time()

            drop_table(cursor)

            cursor.close()
        except Exception:
            drop_table(cursor)
            exit(1)

        return end_time - start_time, end_exec - start_exec, len(rows)


if __name__ == '__main__':
    connection_info = {
        'host': '127.0.0.1',
        'port': 5433,
        'user': 'dbadmin',
        'password': '',
        'database': 'docker',
        'autocommit': True,
    }
    logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")

    logging.info(f'Time taken to write: {write_speed_test(10000)} sec')

    read_time, upd_time, num_rows = read_speed_test()
    logging.info(f'Time taken to read {num_rows} rows: {read_time} sec')
    logging.info(f'Time taken to update 100 rows: {upd_time} sec')


