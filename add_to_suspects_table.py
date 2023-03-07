import psycopg2
import psycopg2.extras
from psycopg2.extensions import AsIs
import datetime
import random
import requests


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

    result = cursor.fetchone() # assuming every LP has one owner
    if (result):
        cursor.execute("SELECT * FROM sensors.suspects WHERE person_id = " + str(result['person_id']))
        suspectResult = cursor.fetchone()

        if (suspectResult):
            update_statement = "UPDATE sensors.suspects SET sensor_id=%s, timestamp=%s, " \
                               "sensor_location_x=%s, sensor_location_y=%s WHERE person_id = " + str(result['person_id'])
            cursor.execute(update_statement, (report['sensor_id'], report['timestamp'],
                                              report['sensor_location_x'], report['sensor_location_y']))
            conn.commit()
        else:
            wantedLevel = getWantedLevel()

            result['sensor_id'] = report['sensor_id']
            result['timestamp'] = report['timestamp']
            result['sensor_location_x'] = report['sensor_location_x']
            result['sensor_location_y'] = report['sensor_location_y']
            result['wanted_level'] = wantedLevel
            columns = result.keys()
            values = [result[column] for column in columns]

            insert_statement = 'INSERT INTO sensors.suspects (%s) VALUES %s'
            query = cursor.mogrify(insert_statement, (AsIs(','.join(columns)), tuple(values)))
            cursor.execute(query)
            conn.commit()

            if(wantedLevel > 1):
                sendLicensePlate(result['license_plates'])

                wantedRecord = {
                    "person_id": result['person_id'],
                    "photo_url": result['photo_url'], #check if its text or bytea
                    "first_name": result['first_name'],
                    "last_name": result['last_name'],
                    "address": result['address'],
                    "city": result['city'],
                    "wanted": result['wanted'],
                    "wanted_level": result['wanted_level'],
                    "actions": result['actions'],
                    "license_plates": result['license_plates'],
                    # "car_model": "", # we dont have that field
                }

                columns = wantedRecord.keys()
                values = [wantedRecord[column] for column in columns]

                insert_statement = 'INSERT INTO sensors.wanted (%s) VALUES %s'
                query = cursor.mogrify(insert_statement, (AsIs(','.join(columns)), tuple(values)))
                cursor.execute(query)
                conn.commit()

    conn.close()


def sendLicensePlate(lp):
    #TODO need info from other team
    IP = ""
    PORT = ""

    url = 'http://%s:%s/license-plates' % (IP, PORT)
    request = {'plate_number': lp}

    # res = requests.post(url, json=request)
    # return res.text


#TODO: connect to BI
def getWantedLevel():
    return random.randint(1, 3)


if __name__ == '__main__':
    exampleReport = {
        'number': '80-UJI-95',
        'sensor_id': 'sensor',
        'timestamp': datetime.datetime.now(),
        'sensor_location_x': 1,
        'sensor_location_y': 100
    }

    #TODO connect to the BODEL
    addToSuspectTable(exampleReport)
