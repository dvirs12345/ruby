import psycopg2
import psycopg2.extras
from psycopg2.extensions import AsIs
import datetime


def addToSuspectTable(report):
    conn = psycopg2.connect(
        database="postgres",
        user='postgres',
        password='bagrut3',
        host='10.252.30.4',
        port='5432'
    )

    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
    cursor.execute("SELECT * FROM sensors.person WHERE '" + report['number'] + "' = any (license_plates);")

    result = cursor.fetchone()  # assuming every LP has one owner
    if result:
        result['sensor_id'] = report['sensor_id']
        result['timestamp'] = report['timestamp']
        result['sensor_location_x'] = report['sensor_location_x']
        result['sensor_location_y'] = report['sensor_location_y']

        columns = result.keys()
        values = [result[column] for column in columns]

        cursor.execute("SELECT * FROM sensors.suspects WHERE person_id = " + str(result['person_id']))
        result = cursor.fetchone()
        if result:
            update_statement = "UPDATE sensors.suspects SET sensor_id=%s, timestamp=%s, " \
                               "sensor_location_x=%s, sensor_location_y=%s WHERE person_id = " + \
                               str(result['person_id'])
            cursor.execute(update_statement, (report['sensor_id'], report['timestamp'],
                                              report['sensor_location_x'], report['sensor_location_y']))
            conn.commit()
        else:
            insert_statement = 'INSERT INTO sensors.suspects (%s) VALUES %s'
            query = cursor.mogrify(insert_statement, (AsIs(','.join(columns)), tuple(values)))
            cursor.execute(query)
            conn.commit()
    conn.close()


if __name__ == '__main__':
    exampleReport = {
        'number': '05-B-8296',
        'sensor_id': 'sensor',
        'timestamp': datetime.datetime.now(),
        'sensor_location_x': 1,
        'sensor_location_y': 100
    }

    addToSuspectTable(exampleReport)
