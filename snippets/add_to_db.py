import json
import psycopg2
from psycopg2.extensions import AsIs
from psycopg2.pool import ThreadedConnectionPool
import threading
import time

DATA_INDEX = 1
ID_INDEX = 0
MAX_CONNECTIONS = 40

tcp = ThreadedConnectionPool(
    1,
    MAX_CONNECTIONS,
    database="postgres",
    user='postgres',
    password='bagrut3',
    host='10.252.30.4',
    port='5432'
)


def insert_to_db(dict_chunk):
    insert = 'insert into sensors.person (%s) values %s'
    conn = tcp.getconn()
    cursor = conn.cursor()

    for item in dict_chunk.items():
        person_id = item[ID_INDEX]

        cursor.execute("SELECT person_id FROM sensors.person WHERE person_id = %s", (person_id,))

        if cursor.fetchone() is not None:
            continue

        person_info = item[DATA_INDEX]

        db_data = person_info
        db_data["person_id"] = person_id
        db_data.pop('sensors_activity')

        if db_data["wanted"] == "":
            db_data["wanted"] = False

        l = [(c, v) for c, v in db_data.items()]
        columns = ','.join([t[0] for t in l])
        values = tuple([t[1] for t in l])

        query = cursor.mogrify(insert, ([AsIs(columns)] + [values]))

        cursor.execute(query)

    conn.commit()
    tcp.putconn(conn)
    print("thread done")


if __name__ == '__main__':
    threads = []

    with open("population_registry.json", encoding="utf8") as json_file:
        loaded_json = json.load(json_file)
        current_index = 0
        increment_rate = 100

        while len(loaded_json) >= current_index:
            if current_index + increment_rate > len(loaded_json):
                current_index = len(loaded_json) - 1 - increment_rate
            current_chunk = dict(list(loaded_json.items())[current_index:current_index + increment_rate])

            current_thread = threading.Thread(target=insert_to_db, args=(current_chunk,))
            threads.append(current_thread)

            while threading.active_count() >= MAX_CONNECTIONS:
                time.sleep(1)

            current_thread.start()
            current_index += increment_rate

        for currentThread in threads:
            currentThread.join()

        print("finished")

