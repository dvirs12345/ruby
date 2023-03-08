import add_to_suspects_table
import readLicenecePlate
import psycopg2
import threading
import numpy as np
from psycopg2.pool import ThreadedConnectionPool

#reportsThread = threading.Thread(target=add_to_suspects_table.listenForReports())
#reportsThread.start()

MAX_CONNECTIONS = 55

tcp = ThreadedConnectionPool(
    1,
    MAX_CONNECTIONS,
    database="postgres",
    user='postgres',
    password='bagrut3',
    host='10.252.30.4',
    port='5432'
)

def getReport(image):
    open("FromDB.jpg", 'wb').write(image[-2])
    number_plate = readLicenecePlate.getLicensePlate()
    print(number_plate)
    report = {
        'number': number_plate,
        'sensor_id': image[1],
        'timestamp': image[-1],
        'sensor_location_x': image[2],
        'sensor_location_y': image[3]
    }

    return report


def insertToDB(reports):
    conn = tcp.getconn()
    add_to_suspects_table.addToSuspectTable(reports, conn)
    tcp.putconn(conn)


if __name__ == '__main__':
    connection = psycopg2.connect(
        database="postgres",
        user='postgres',
        password='bagrut3',
        host='10.252.30.4',
        port='5432'
    )

    cursor = connection.cursor()

    cursor.execute(str("SELECT * FROM sensors.images"))
    data = cursor.fetchall()

    reports = []

    for image in data:
        reports.append(getReport(image))

    splittedReports = np.array_split(reports, MAX_CONNECTIONS)

    threads = []

    for report in splittedReports:
        addSuspect = threading.Thread(target=insertToDB, args=(reports,))
        threads.append(addSuspect)
        addSuspect.start()

    for thread in threads:
        print(thread)
        thread.join()
